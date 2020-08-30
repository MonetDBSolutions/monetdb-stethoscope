# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""
The purpose of data obfuscation is to not show data values or SQL object identifiers
to the outside user. Although relevant mostly for end-user interaction with
a result set, it can also be applied to the events spit out by MonetDB for
post analysis.

For a good introduction to data obfuscation techniques consider
http://blough.ece.gatech.edu/research/papers/ieeesp04.pdf

Complete data obfuscation is best implemented with simply masking all literals in a trace a pattern, e.g. ***
This method is supported by the stethoscope using the -T masking option.

The disadvantage of data masking is that too much is shielded for post-analysis of the system behavior.
A better solution is to use one-way functions, which are also the cornerstone for all
encryption techniques. In general, it is a function of the form f(x)= s * y, where 's' is
considered the secret key. Only if you have more than on pair (x,f(x) it can be broken.
To reduce the impact of this out of bound leakage oa the secret key, its value is
a fresh random number chosen at the start of the trace. Using multiple keys, geared
at a class of values further reduce the potential of leakage.

Furthermore, this mapping is only applied to data that originates in the
database or can be derived from the database by applying an expression.
In its simpliest form a data item is processed by a function that respects
the properties of the underlying domain type, but makes it practially impossible
to invert the original value from the message.

The new obfuscation scheme designed here relies on two elements.
1) DDL obfuscation. Which maps all SQL schema objects to a non-informative alternative.
For example, the column reference finances.personal.salary is mapped to a patter
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
    obfuscate = {}
    mapping = {}
    schema_mapping = {}
    table_mapping = {}
    column_mapping = {}
    object_mapping = {}

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
        self.schema_mapping = dict()
        self.table_mapping = dict()
        self.column_mapping = dict()

    # obfuscation is MAL instruction specific
    def __call__(self, json_object):
        rdict = dict(json_object)
        varlist = rdict.get("args", [])

        # map schema information
        if rdict['module'] == 'sql' and (rdict['function'] == 'bind' or rdict['function'] == 'bind_idx'):
            varlist[2]["value"] = self.obfuscate_schema(varlist[2]["value"])
            varlist[3]["value"] = self.obfuscate_table(varlist[3]["value"])
            varlist[4]["value"] = self.obfuscate_column(varlist[4]["value"])

        # map selections and arithmetics
        elif rdict['module'] == 'algebra' and rdict['function'] == 'thetaselect':
            varlist[3]["value"] = self.obfuscate_data(varlist[3]["value"], varlist[3]["type"])

        elif rdict['module'] == 'algebra' and rdict['function'] == 'select':
            varlist[3]["value"] = self.obfuscate_data(varlist[3]["value"], varlist[3]["type"])
            varlist[4]["value"] = self.obfuscate_data(varlist[4]["value"], varlist[4]["type"])

        # extend the list with other classes of MAL operations
        else:
            for var in varlist:
                # hide the table information
                alias = var.get("alias")
                s, t, c = alias.split('.')
                s = self.obfuscate_schema(s)
                t = self.obfuscate_table(s)
                c = self.obfuscate_column(s)
                var["alias"] = '.'.join([s, t, c])
        return rdict

    def obfuscate_object(self, original, kind):
        name = kind[:3] + original
        if name in self.mapping:
            return self.mapping[name]
        picked = self.obfuscate[kind]
        self.mapping[name] = f"{kind}{picked}"
        self.obfuscate[kind] = self.obfuscate[kind] + 1
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

    def obfuscate_data(self, original, tpe):
        if tpe not in self.mapping:
            self.mapping.update({tpe: random.randint() % 37})
        if tpe == ':str':
            picked = '***'
        else:
            picked = original * self.mapping[tpe]
        return picked

    def obfuscate_sql(self, original):
        # parse the SQL statement and replace sensitive componenta
        return '***'
