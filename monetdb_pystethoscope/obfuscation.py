# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""
The purpose of data obfuscation is to not show data values or SQL object identifiers
to the outside user. Although relevant mostly for end-user interaction with
a result set, it can also be applied to the events spit out by MonetDB for
post session analysis and system monitoring.

For a good introduction to data obfuscation techniques consider
http://blough.ece.gatech.edu/research/papers/ieeesp04.pdf

Complete data obfuscation is best implemented with simply masking all literals in a query plan a pattern, e.g. ***
This method is supported by the stethoscope using the -t obfuscation option.

The disadvantage of data masking is that too much is shielded for post-analysis of the system behavior.
A better solution is to use one-way functions, which are also the cornerstone for all
encryption techniques. In general, it is a function of the form f(x)= s * y, where 's' is
considered the secret key. Only if you have a pair (x,f(x) it can be broken.
To reduce the impact of this out of bound leakage of the secret key, its value is
a fresh random number chosen at the start of the trace. Using multiple keys, geared
at a class of values further reduce the potential of leakage.

Furthermore, this mapping is only applied to data that originates in the
database or can be derived from the database by applying an expression.
In its simpliest form a data item is processed by a function that respects
the properties of the underlying domain type, but makes it practically impossible
to invert the original value from the message.

The new obfuscation scheme designed here relies on two elements.
1) DDL obfuscation. Which maps all SQL schema objects to a non-informative alternative.
For example, the column reference finances.personal.salary is mapped to a pattern
schema<S>.table<T>.Column<C> where S,T,C are randomized numbers, whose validity
only holds for a single stethoscope run.

2) Query parameter obfuscation.
The arguments to operators that find their origin in the database are
mapped using a one-way function
    f_type(original) = random * original
where random is different for each column/type and holds for a single stethoscope run.
The type specific obfuscation can lead to an overflow, which renders the
relative ordering within a range predicate meaningless.

The code below is considered a default. It should be easy for the user
to replace it with partial masking or alternative obfuscation schemes.

Beware, the stethoscope only sees the data presented in the queries, which
may not even reflect an item in the database. As such, it is more about
obfuscation of the kind of queries posed to the system at stake.

WARNING the output of the obfuscation should not include recognizable 'filename' with
system paths, 'alias' with recognizable schema information, 'sql.bind' should not
show schema information, ... values in selections and likeselect should not be
recognizable.

"""
import random


class ObfuscateTransformer:
    """The default is to replace every literal value in the plan with three asterisks."""
    debug = False
    secrets = {}
    mapping = {}

    def __init__(self):
        # The types which we are censoring
        self._types = [
            # "bit",
            "bte",
            "sht",
            "int",
            "lng",
            "hge",
            "oid",
            "flt",
            "dbl",
            "str",
            "color",
            "date",
            "daytime",
            "time",
            "timestamp",
            "timezone",
            "blob",
            "inet",
            "url",
            "json",
            "uuid"
        ]

    # obfuscation is MAL instruction specific
    def __call__(self, json_object):
        rdict = dict(json_object)
        if ObfuscateTransformer.debug:
            print("OBFUSCATE", rdict)
        varlist = rdict.get("args", [])

        # map schema information, everything that comes directly from the SQL layer is suspect
        if 'module' in rdict:
            if rdict['module'] == 'sql' and (rdict['function'] == 'bind' or rdict['function'] == 'bind_idx'):
                varlist[2]["value"] = self.obfuscate_schema(varlist[2].get("value"))
                varlist[3]["value"] = self.obfuscate_table(varlist[3].get("value"))
                varlist[4]["value"] = self.obfuscate_column(varlist[4].get("value"))
                rdict['args'] = varlist
                return rdict
            if rdict['module'] == 'sql' and \
                    rdict['function'] in ['tid', 'append', 'delete', 'emptybindidx', 'emptybind']:
                varlist[2]["value"] = self.obfuscate_schema(varlist[2].get("value"))
                varlist[3]["value"] = self.obfuscate_table(varlist[3].get("value"))
                if len(varlist) > 4:
                    varlist[4]["value"] = self.obfuscate_column(varlist[4].get("value"))
                rdict['args'] = varlist
                return rdict
            if rdict['module'] == 'sql' and rdict['function'] == 'clear_table':
                varlist[1]["value"] = self.obfuscate_schema(varlist[1].get("value"))
                varlist[2]["value"] = self.obfuscate_table(varlist[2].get("value"))
                rdict['args'] = varlist
                return rdict
            if rdict['module'] == 'sql' and rdict['function'] == 'deltas':
                varlist[1]["value"] = self.obfuscate_schema(varlist[1].get("value"))
                varlist[2]["value"] = self.obfuscate_table(varlist[2].get("value"))
                if len(varlist) > 3:
                    varlist[3]["value"] = self.obfuscate_column(varlist[3].get("value"))
                rdict['args'] = varlist
                return rdict
            if rdict['module'] == 'sql' and rdict['function'] in ['setVariable', 'getVariable']:
                varlist[3]["value"] = self.obfuscate_variable(varlist[2])
                rdict['args'] = varlist
                return rdict

            # selection operators are based on used-defined data
            if rdict['module'] == 'algebra' and rdict['function'] in ['thetaselect']:
                if len(varlist) == 4:
                    varlist[2]["value"] = self.obfuscate_data(varlist[3])
                else:
                    varlist[3]["value"] = self.obfuscate_data(varlist[3])
                rdict['args'] = varlist
                return rdict
            if rdict['module'] == 'algebra' and rdict['function'] in ['select'] and len(varlist) == 7:
                varlist[2]["value"] = self.obfuscate_data(varlist[2])
                varlist[3]["value"] = self.obfuscate_data(varlist[3])
                rdict['args'] = varlist
                return rdict
            if rdict['module'] == 'algebra' and rdict['function'] in ['select'] and len(varlist) == 8:
                varlist[3]["value"] = self.obfuscate_data(varlist[3])
                varlist[4]["value"] = self.obfuscate_data(varlist[4])
                rdict['args'] = varlist
                return rdict
            if rdict['module'] == 'algebra' and rdict['function'] in ['find', 'project']:
                varlist[2]["value"] = self.obfuscate_data(varlist[2])
                rdict['args'] = varlist
                return rdict
            if rdict['module'] == 'algebra' and rdict['function'] in ['project'] and varlist[2].get("const") == 1:
                varlist[2]["value"] = self.obfuscate_data(varlist[2])
                rdict['args'] = varlist
                return rdict
            if rdict['module'] == 'algebra' and rdict['function'] in ['likeselect']:
                varlist[3]["value"] = self.obfuscate_data(varlist[3])
                rdict['args'] = varlist
                return
            if rdict['module'] == 'algebra' and \
                    rdict['function'] in ['calc', 'batmmath', 'mmath', 'batstr', 'inspect'] and \
                    rdict['type'] != 'uuid':
                vl = []
                for var in varlist:
                    vl.append(self.obfuscate_data(var))
                rdict['args'] = vl
                return rdict

        # extend the list with other classes of MAL operations
        vl = []
        for var in varlist:
            # hide the table information
            alias = var.get("alias")
            if alias:
                s, t, c = alias.split('.')
                s = self.obfuscate_schema(s)
                t = self.obfuscate_table(s)
                c = self.obfuscate_column(s)
                var["alias"] = '.'.join([s, t, c])
            filename = var.get("file")
            if filename:
                var["file"] = self.obfuscate_file(filename)
            vl.append(var)
        rdict['args'] = vl
        return rdict

    def obfuscate_full(self, varlist):
        for var in varlist:
            if 'value' in var:
                var.update({'value': self.obfuscate_data(var)})

    def obfuscate_object(self, original, kind):
        if not original:
            return kind
        if kind not in self.secrets:
            self.secrets.update({kind: random.randint(0, 11)})
        name = str(kind) + str(original)
        if name in self.mapping:
            return self.mapping[name]
        picked = kind[:3] + str(self.secrets[kind])
        self.mapping[name] = picked
        self.secrets[kind] = self.secrets[kind] + 1
        return picked

    # Obfuscation of the SQL objects
    def obfuscate_schema(self, original):
        res = self.obfuscate_object(original, 'sch')
        if ObfuscateTransformer.debug:
            print('OBFUSCATE SHEMA ', original, res)
        return res

    def obfuscate_table(self, original):
        res = self.obfuscate_object(original, 'tbl')
        if ObfuscateTransformer.debug:
            print('OBFUSCATE TABLE ', original, res)
        return res

    def obfuscate_column(self, original):
        res = self.obfuscate_object(original, 'col')
        if ObfuscateTransformer.debug:
            print('OBFUSCATE COLUMN ', original, res)
        return res

    def obfuscate_procedure(self, original):
        res = self.obfuscate_object(original, 'proc')
        if ObfuscateTransformer.debug:
            print('OBFUSCATE PROCEDURE ', original, res)
        return res

    def obfuscate_file(self, original):
        if original.startswith('tmp_'):
            return original
        res = self.obfuscate_object(original, 'file')
        if ObfuscateTransformer.debug:
            print('OBFUSCATE FILE ', original, res)
        return res

    def obfuscate_variable(self, arg):
        # only a limited number of variables are allowed to expose their value
        original = arg['value']
        if original in ['optimizer', 'sql_debug', 'debug']:
            return original
        res = self.obfuscate_data(arg)
        if ObfuscateTransformer.debug:
            print('OBFUSCATE VARIABLE ', original, res)
        return res

    def obfuscate_string(self, original):
        # keep the length of the string, map all non-white characters
        if 'string' not in self.mapping:
            secret = list('abcdefghijklmnopqrstuvwxyz')
            random.shuffle(secret)
            self.mapping.update({'string': secret})
        if not original:
            if ObfuscateTransformer.debug:
                print('OBFUSCATE STRING ', original, 'None')
            return ''
        secret = self.mapping['string']
        new = ''.join([secret[ord(c) % len(secret)] for c in original])
        random.shuffle(secret)
        self.mapping.update({'string': secret})
        if ObfuscateTransformer.debug:
            print('OBFUSCATE STRING ', original, new)
        return new

    def obfuscate_data(self, arg):
        original = arg['value']
        tpe = arg('type')
        if not tpe or not original:
            return '****'
        if tpe not in self.mapping:
            self.mapping.update({tpe: random.randint(0, 37)})

        if original in ['null', 'true', 'false']:
            return original
        if tpe in ['str', 'uuid']:
            picked = self.obfuscate_string(original)
        elif tpe in [ "bte", "sht", "int", "lng", "hge"]:
            picked = int(original) * self.mapping[tpe]
        elif tpe in ["flt", "dbl"]:
            picked = float(original) * self.mapping[tpe]
        elif tpe in ["oid", "void"]:
            picked = original
        else:
            picked = '***'
        return picked

    def obfuscate_sql(self, original):
        # parse the SQL statement and replace sensitive components
        print('original', self, original)
        return '***'
