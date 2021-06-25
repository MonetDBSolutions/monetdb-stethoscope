# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

import logging
import re
import random
from monetdb_stethoscope import DEVELOPMENT__


LOGGER = logging.getLogger(__name__)


class ObfuscateTransformer:
    """The default is to replace every literal value in the plan with three asterisks."""
    secrets = {}    # contains the type specific secret keys
    # we initialize the mapping with some general MonetDB specific identifiers.
    mapping = {
        "sys": "sys",
        "tmp": "tmp",
        "env": "env",
        "gdk_dbpath": "gdk_dbpath",
        "mapi_port": "mapi_port",
        "sql_optimizer": "sql_optimizer",
        "sql_debug": "sql_debug",
        "raw_strings": "raw_strings",
        "merovingian_uri": "merovingian_uri",
        "map_listenaddr": "map_listenaddr",
        "mapi_socket": "mapi_socket",
        "monet_vault_key'": "monet_vault_key'",
        "gdk_nr_threads": "gdk_nr_threads",
        "mal_clients": "mal_clients",
        "gdk_dbname": "gdk_dbname",
        "monet_pid": "monet_pid",
        "monet_version": "monet_version",
        "revision": "revision",
        "monet_release": "monet_release",
    }

    pat3 = re.compile(r'([\w_][_\w\d]*|[0-9]+|[\'\"](.*?)[\'\"]+|\W+)')

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
        if DEVELOPMENT__:
            LOGGER.debug("OBFUSCATE %s", rdict)
        varlist = rdict.get("args", [])

        # hunt for the alias properties and replace them everywhere
        vl = []
        for var in varlist:
            # hide the table information
            alias = var.get("alias")
            if alias:
                s, t, c = alias.split('.')
                s = self.obfuscate_schema(s)[1:-1]
                t = self.obfuscate_table(s)[1:-1]
                c = self.obfuscate_column(s)[1:-1]
                var["alias"] = '.'.join([s, t, c])
            filename = var.get("file")
            if filename:
                var["file"] = self.obfuscate_file(filename)
            vl.append(var)
        rdict['args'] = vl

        varlist = rdict.get("args", [])

        # map schema information, everything that comes directly from the SQL layer is suspect
        if 'module' in rdict:
            if rdict['module'] == 'querylog' and rdict['function'] == 'define':
                varlist[1]["value"] = self.obfuscate_sql(varlist[1].get("value"))
                rdict['args'] = varlist
                return rdict

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
                varlist[7]["value"] = self.obfuscate_schema(varlist[7].get("value"))
                if len(varlist) > 7:
                    varlist[8]["value"] = self.obfuscate_table(varlist[8].get("value"))
                if len(varlist) > 8:
                    varlist[9]["value"] = self.obfuscate_column(varlist[9].get("value"))
                rdict['args'] = varlist
                return rdict
            if rdict['module'] == 'sql' and rdict['function'] in ['setVariable', 'getVariable']:
                varlist[3]["value"] = self.obfuscate_variable(varlist[2])
                rdict['args'] = varlist
                return rdict
            if rdict['module'] == 'sql' and rdict['function'] in ['copy_from', 'copy_to']:
                varlist[-7]["value"] = self.obfuscate_string(varlist[-7])
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
            if rdict['module'] == 'calc':
                vl = []
                for var in varlist:
                    vl.append(self.obfuscate_data(var))
                rdict['args'] = vl
                return rdict
        return rdict

    def obfuscate_full(self, varlist):
        for var in varlist:
            if 'value' in var:
                var.update({'value': self.obfuscate_data(var)})

    def obfuscate_object(self, original, kind):
        if not original:
            return kind
        name = kind[:3] + original
        if name in self.mapping:
            return self.mapping[name]
        if kind not in self.secrets:
            self.secrets.update({kind: random.randint(0, 11)})

        picked = kind[:3] + str(self.secrets[kind])
        self.mapping[name] = picked
        self.secrets[kind] = self.secrets[kind] + 1
        return picked

    def obfuscate_schema(self, original):
        if original.strip() in ['sys', '"sys"', 'tmp', '"tmp"']:
            return original.strip()
        res = '"' + self.obfuscate_object(original, 'sch') + '"'
        if DEVELOPMENT__:
            LOGGER.debug('OBFUSCATE SHEMA %s %s', original, res)
        return res

    def obfuscate_table(self, original):
        res = self.obfuscate_object(original, 'tbl')
        if DEVELOPMENT__:
            LOGGER.debug('OBFUSCATE TABLE %s %s', original, res)
        return res

    def obfuscate_column(self, original):
        res = self.obfuscate_object(original, 'col')
        if DEVELOPMENT__:
            LOGGER.debug('OBFUSCATE COLUMN ', original, res)
        return res

    def obfuscate_procedure(self, original):
        res = self.obfuscate_object(original, 'proc')
        if DEVELOPMENT__:
            LOGGER.debug('OBFUSCATE PROCEDURE ', original, res)
        return res

    def obfuscate_file(self, original):
        if original.startswith('tmp_'):
            return original
        if original.startswith('sql_empty'):
            return original
        comp = original.split('bat')
        if len(comp) == 2:
            return comp[1]
        res = self.obfuscate_object(original, 'file')
        if DEVELOPMENT__:
            LOGGER.debug('OBFUSCATE FILE ', original, res)
        return res

    def obfuscate_variable(self, arg):
        # only a limited number of variables are allowed to expose their value
        original = arg['value']
        if original in ['optimizer', 'sql_debug', 'debug']:
            return original
        res = self.obfuscate_object(original, 'var')
        if DEVELOPMENT__:
            LOGGER.debug('OBFUSCATE VARIABLE ', original, res)
        return res

    def obfuscate_string(self, original):
        # keep the length of the string, map all non-white characters
        if not original:
            if DEVELOPMENT__:
                LOGGER.debug('OBFUSCATE STRING ', original, 'None')
            return ''
        if original in ['gdk_dbpath', 'mapi_port', 'sql_optimizer', 'sql_debug', 'raw_strings',
                        'merovingian_uri', 'map_listenaddr', 'mapi_socket', 'monet_vault_key',
                        'gdk_nr_threads', 'mal_clients', 'gdk_dbname', 'monet_pid', 'revision', 'monet_release']:
            return original
        if original in self.mapping:
            return self.mapping[original]

        if 'string' not in self.secrets:
            secret = list('abcdefghijklmnopqrstuvwxyz')
            random.shuffle(secret)
            self.secrets.update({'string': secret})

        secret = self.secrets['string']
        picked = '"' + ''.join([secret[ord(c) % len(secret)] for c in original]) + '"'
        self.mapping.update({original: picked})
        if DEVELOPMENT__:
            LOGGER.debug('OBFUSCATE STRING ', original, picked)
        return picked

    # temporal element are characterwise morphed creating wrong months..days...
    def obfuscate_temporal(self, original, tpe):
        if original in self.mapping:
            return self.mapping['original']
        if tpe not in self.secrets:
            self.secrets.update({tpe: random.randint(1, 111)})

        secret = self.secrets[tpe]  % 10
        new = []
        for c in original:
            if c.isdigit():
                try:
                    m = int(c) + secret
                    new.append("%d" % m)
                except ValueError as msg:
                    LOGGER.error('ERROR TEMPORAL %s', msg)
                    new.append(c)
            else:
                new.append(c)
        new = ''.join(new)
        self.mapping.update({original: new})
        return new

    def obfuscate_data(self, arg):
        original = arg['value']
        if original in self.mapping:
            return self.mapping[original]

        tpe = arg['type']
        if not tpe or not original:
            return '****'
        if tpe not in self.secrets:
            self.secrets.update({tpe: random.randint(1, 111)})

        if original in ['nil', 'true', 'false']:
            return original

        picked = ''
        if tpe in ['str', 'uuid']:
            picked = self.obfuscate_string(original)
        elif tpe in [ "bte", "sht", "int", "lng", "hge"]:
            try:
                picked = int(original) * self.secrets[tpe]
                self.mapping.update({original: picked})
            except ValueError as msg:
                LOGGER.error('ERROR %s %s', original, msg)
        elif tpe in ["flt", "dbl"]:
            try:
                picked = float(original) * self.secrets[tpe]
                self.mapping.update({original: picked})
            except ValueError as msg:
                LOGGER.error('ERROR %s %s', original, msg)
        elif tpe in ["oid", "void"]:
            picked = original
        elif tpe in ["date", "daytime", "time", "timestamp", "timezone"]:
            picked = self.obfuscate_temporal(original, tpe)
        else:
            picked = '***'
        return picked

    # SQL obfuscation should be focused on all non-reserved identifiers
    keywords = [
        "false", "true", "ALTER", "ADD", "AND",
        "RANK", "DENSE_RANK", "PERCENT_RANK", "CUME_DIST", "ROW_NUMBER",
        "NTILE", "LAG", "LEAD", "FIRST_VALUE", "LAST_VALUE",
        "NTH_VALUE", "BEST", "EFFORT", "AS", "ASC",
        "AUTHORIZATION", "BETWEEN", "SYMMETRIC", "ASYMMETRIC", "BY",
        "CAST", "CONVERT", "CHARACTER", "CHAR", "VARYING",
        "VARCHAR", "BINARY", "LARGE", "OBJECT", "CLOB",
        "BLOB", "TEXT", "TINYTEXT", "STRING", "CHECK",
        "CLIENT", "SERVER", "COMMENT", "CONSTRAINT", "CREATE",
        "CROSS", "COPY", "RECORDS", "DELIMITERS", "STDIN",
        "STDOUT", "TINYINT", "SMALLINT", "INTEGER", "INT",
        "MEDIUMINT", "BIGINT", "HUGEINT", "DEC", "DECIMAL",
        "NUMERIC", "DECLARE", "DEFAULT", "DESC", "DISTINCT",
        "DOUBLE", "REAL", "DROP", "ESCAPE", "EXISTS",
        "UESCAPE", "EXTRACT", "FLOAT", "FOR", "FOREIGN",
        "FROM", "FWF", "REFERENCES", "MATCH", "FULL",
        "PARTIAL", "SIMPLE", "INSERT", "UPDATE", "DELETE",
        "TRUNCATE", "MATCHED", "ACTION", "CASCADE", "RESTRICT",
        "FIRST", "GLOBAL", "GROUP", "GROUPING", "ROLLUP",
        "CUBE", "HAVING", "ILIKE", "IMPRINTS", "IN",
        "INNER", "INTO", "IS", "JOIN", "KEY",
        "LATERAL", "LEFT", "LIKE", "LIMIT", "SAMPLE",
        "SEED", "LAST", "LOCAL", "LOCKED", "NATURAL",
        "NOT", "NULL", "NULLS", "OFFSET", "ON",
        "OPTIONS", "OPTION", "OR", "ORDER", "ORDERED",
        "OUTER", "OVER", "PARTITION", "PATH", "PRECISION",
        "PRIMARY", "USER", "RENAME", "UNENCRYPTED", "ENCRYPTED",
        "PASSWORD", "GRANT", "REVOKE", "ROLE", "ADMIN",
        "PRIVILEGES", "PUBLIC", "CURRENT_USER", "CURRENT_ROLE", "SESSION_USER",
        "CURRENT_SCHEMA", "SESSION", "RIGHT", "SCHEMA", "SELECT",
        "SET", "SETS", "AUTO_COMMIT", "ALL", "ANY",
        "SOME", "EVERY", "COLUMN", "TABLE", "TEMPORARY",
        "TEMP", "STREAM", "REMOTE", "MERGE", "REPLICA",
        "TO", "UNION", "EXCEPT", "INTERSECT", "CORRESPONDING",
        "UNIQUE", "USING", "VALUES", "VIEW", "WHERE",
        "WITH", "DATA", "DATE", "TIME", "TIMESTAMP",
        "INTERVAL", "CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP", "CURRENT_TIMEZONE",
        "NOW", "LOCALTIME", "LOCALTIMESTAMP", "ZONE", "CENTURY",
        "DECADE", "YEAR", "QUARTER", "MONTH", "WEEK",
        "DOW", "DOY", "DAY", "HOUR", "MINUTE",
        "SECOND", "EPOCH", "POSITION", "SUBSTRING", "SPLIT_PART",
        "CASE", "WHEN", "THEN", "ELSE", "END",
        "NULLIF", "COALESCE", "ELSEIF", "IF", "WHILE",
        "DO", "COMMIT", "ROLLBACK", "SAVEPOINT", "RELEASE",
        "WORK", "CHAIN", "PRESERVE", "ROWS", "NO",
        "START", "TRANSACTION", "READ", "WRITE", "ONLY",
        "ISOLATION", "LEVEL", "UNCOMMITTED", "COMMITTED", "REPEATABLE",
        "SERIALIZABLE", "DIAGNOSTICS", "SIZE", "STORAGE", "TYPE",
        "PROCEDURE", "FUNCTION", "LOADER", "REPLACE", "FILTER",
        "AGGREGATE", "RETURNS", "EXTERNAL", "NAME", "RETURN",
        "CALL", "LANGUAGE", "ANALYZE", "MINMAX", "EXPLAIN",
        "PLAN", "DEBUG", "TRACE", "PREPARE", "PREP",
        "EXECUTE", "EXEC", "DEALLOCATE", "INDEX", "SEQUENCE",
        "RESTART", "INCREMENT", "MAXVALUE", "MINVALUE", "CYCLE",
        "CACHE", "NEXT", "VALUE", "GENERATED", "ALWAYS",
        "IDENTITY", "SERIAL", "BIGSERIAL", "AUTO_INCREMENT", "CONTINUE",
        "TRIGGER", "ATOMIC", "BEGIN", "OF", "BEFORE",
        "AFTER", "ROW", "STATEMENT", "NEW", "OLD",
        "EACH", "REFERENCING", "RANGE", "UNBOUNDED", "PRECEDING",
        "FOLLOWING", "CURRENT", "EXCLUDE", "OTHERS", "TIES",
        "GROUPS", "WINDOW", "XMLCOMMENT", "XMLCONCAT", "XMLDOCUMENT",
        "XMLELEMENT", "XMLATTRIBUTES", "XMLFOREST", "XMLPARSE", "STRIP",
        "WHITESPACE", "XMLPI", "XMLQUERY", "PASSING", "XMLTEXT",
        "NIL", "REF", "ABSENT", "DOCUMENT", "ELEMENT",
        "CONTENT", "XMLNAMESPACES", "NAMESPACE", "XMLVALIDATE", "RETURNING",
        "LOCATION",  "ACCORDING", "XMLSCHEMA", "URI",
        "XMLAGG", "GEOMETRY", "POINT", "LINESTRING", "POLYGON",
        "MULTIPOINT", "MULTILINESTRING", "MULTIPOLYGON", "GEOMETRYCOLLECTION", "POINTZ",
        "LINESTRINGZ", "POLYGONZ", "MULTIPOINTZ", "MULTILINESTRINGZ", "MULTIPOLYGONZ",
        "GEOMETRYCOLLECTIONZ", "POINTM", "LINESTRINGM", "POLYGONM", "MULTIPOINTM",
        "MULTILINESTRINGM", "MULTIPOLYGONM", "GEOMETRYCOLLECTIONM", "POINTZM", "LINESTRINGZM",
        "POLYGONZM", "MULTIPOINTZM", "MULTILINESTRINGZM", "MULTIPOLYGONZM", "GEOMETRYCOLLECTIONZM",

        # Also add the main math functions
        "POWER", "FLOOR", "CEIL", "CEILING", "SIN",
        "COS", "TAN", "ASIN", "ACOS", "ATAN",
        "COT", "COSH", "TANH", "SQRT", "CBRT",
        "EXP", "LOG", "LOG10", "LOG2", "DEGRESS",
        "RADIANS", "RAND",
    ]

    #  the property strong can be set to avoid any mapping of names/literals
    def obfuscate_sql(self, original, strong=False):
        #  mask all except keywords and operators to retain structure
        # Mask all string literals
        original =  original.strip()
        picked = self.pat3.findall(original)

        nqry = []
        for e in picked:
            t = e[0]
            if t.upper() in ObfuscateTransformer.keywords:
                nqry.append(t.upper())
            elif t[0] == "\\n":
                nqry.append("\\n")
                e = e.next()
            elif t[0] in ["'" , '*', ' ', ',', '.', ';', '(', ')', '[', ']',
                           '+', '-', '/', '*', '%', '@', '!', '#', '$', '^', '&', ':', '|', '\\']:
                nqry.append(t)
            elif not strong and t in ObfuscateTransformer.mapping:
                nqry.append(str(ObfuscateTransformer.mapping[t]))
            else:
                nqry.append('$$$')
        picked = ''.join(nqry)

        if DEVELOPMENT__:
            LOGGER.debug('OBFUSCATE QUERY %s\n%s', original, picked)
        return picked
