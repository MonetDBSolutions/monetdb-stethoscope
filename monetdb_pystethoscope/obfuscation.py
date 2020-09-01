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

"""
import random


class ObfuscateTransformer:
    """The default is to replace every literal value in the plan with three asterisks."""
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
        varlist = rdict.get("args", [])

        # map schema information
        if 'module' in rdict:
            if rdict['module'] == 'sql' and (rdict['function'] == 'bind' or rdict['function'] == 'bind_idx'):
                varlist[2]["value"] = self.obfuscate_schema(varlist[2].get("value"))
                varlist[3]["value"] = self.obfuscate_table(varlist[3].get("value"))
                varlist[4]["value"] = self.obfuscate_column(varlist[4].get("value"))
                return
            if rdict['module'] == 'sql' and (rdict['function'] in ['tid', 'append', 'emptybindidx', 'emptybind']):
                varlist[2]["value"] = self.obfuscate_schema(varlist[2].get("value"))
                varlist[3]["value"] = self.obfuscate_table(varlist[3].get("value"))
                if len(varlist) > 4:
                    varlist[4]["value"] = self.obfuscate_column(varlist[4].get("value"))
                return
            if rdict['module'] == 'sql' and rdict['function'] == 'clear_table':
                varlist[1]["value"] = self.obfuscate_schema(varlist[1].get("value"))
                varlist[2]["value"] = self.obfuscate_table(varlist[2].get("value"))
                return
            if rdict['module'] == 'sql' and rdict['function'] == 'deltas':
                varlist[1]["value"] = self.obfuscate_schema(varlist[1].get("value"))
                varlist[2]["value"] = self.obfuscate_table(varlist[2].get("value"))
                if len(varlist) > 3:
                    varlist[3]["value"] = self.obfuscate_column(varlist[3].get("value"))

        # extend the list with other classes of MAL operations
        for var in varlist:
            # hide the table information
            alias = var.get("alias")
            if alias:
                s, t, c = alias.split('.')
                s = self.obfuscate_schema(s)
                t = self.obfuscate_table(s)
                c = self.obfuscate_column(s)
                var["alias"] = '.'.join([s, t, c])
            if 'value' in var:
                var.update({'value': self.obfuscate_data(var.get("value"), var.get("type"))})
        return rdict

    def obfuscate_object(self, original, kind):
        if not original:
            return kind
        if kind not in self.secrets:
            self.secrets.update({kind: random.randint(0, 11)})
        name = str(kind[:3]) + str(original)
        if name in self.mapping:
            return self.mapping[name]
        picked = kind[:3] + str(self.secrets[kind])
        self.mapping[name] = picked
        self.secrets[kind] = self.secrets[kind] + 1
        return picked

    # Obfuscation of the SQL objects
    def obfuscate_schema(self, original):
        return self.obfuscate_object(original, 'schema')

    def obfuscate_table(self, original):
        return self.obfuscate_object(original, 'table')

    def obfuscate_column(self, original):
        return self.obfuscate_object(original, 'column')

    def obfuscate_procedure(self, original):
        return self.obfuscate_object(original, 'procedure')

    def obfuscate_string(self, original):
        # keep the length of the string, map all non-white characters
        if 'string' not in self.mapping:
            secret = list('abcdefghijklmnopqrstuvwxyz')
            random.shuffle(secret)
            self.mapping.update({'string': secret})
        if not original:
            return ''
        secret = self.mapping['string']
        new = ''.join([secret[ord(c) % len(secret)] for c in original])
        random.shuffle(secret)
        self.mapping.update({'string': secret})
        return new

    def obfuscate_data(self, original, tpe):
        if not tpe:
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
        return '***'
