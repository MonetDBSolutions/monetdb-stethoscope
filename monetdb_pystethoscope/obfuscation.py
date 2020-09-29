# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

import re
import random
from monetdb_pystethoscope import DEVELOPMENT__


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
        if DEVELOPMENT__:
            print("OBFUSCATE", rdict)
        varlist = rdict.get("args", [])

        # hunt for the alias properties and replace them everywhere
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

    def obfuscate_schema(self, original):
        if original.strip() in ['sys', '"sys"', 'tmp', '"tmp"']:
            return original.strip()
        res = '"' + self.obfuscate_object(original, 'sch') + '"'
        if DEVELOPMENT__:
            print('OBFUSCATE SHEMA ', original, res)
        return res

    def obfuscate_table(self, original):
        res = '"' + self.obfuscate_object(original, 'tbl') + '"'
        if DEVELOPMENT__:
            print('OBFUSCATE TABLE ', original, res)
        return res

    def obfuscate_column(self, original):
        res = '"' + self.obfuscate_object(original, 'col') + '"'
        if DEVELOPMENT__:
            print('OBFUSCATE COLUMN ', original, res)
        return res

    def obfuscate_procedure(self, original):
        res = self.obfuscate_object(original, 'proc')
        if DEVELOPMENT__:
            print('OBFUSCATE PROCEDURE ', original, res)
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
            print('OBFUSCATE FILE ', original, res)
        return res

    def obfuscate_variable(self, arg):
        # only a limited number of variables are allowed to expose their value
        original = arg['value']
        if original in ['optimizer', 'sql_debug', 'debug']:
            return original
        res = self.obfuscate_data(arg)
        if DEVELOPMENT__:
            print('OBFUSCATE VARIABLE ', original, res)
        return res

    def obfuscate_string(self, original):
        # keep the length of the string, map all non-white characters
        if 'string' not in self.mapping:
            secret = list('abcdefghijklmnopqrstuvwxyz')
            random.shuffle(secret)
            self.mapping.update({'string': secret})
        if not original:
            if DEVELOPMENT__:
                print('OBFUSCATE STRING ', original, 'None')
            return ''
        secret = self.mapping['string']
        new = ''.join([secret[ord(c) % len(secret)] for c in original])
        random.shuffle(secret)
        self.mapping.update({'string': secret})
        if DEVELOPMENT__:
            print('OBFUSCATE STRING ', original, new)
        return new

    def obfuscate_temporal(self, original, tpe):
        if tpe not in self.mapping:
            secret = list('01234567890')
            random.shuffle(secret)
            self.mapping.update({tpe: secret})
        secret = self.mapping[tpe]
        new = []
        for c in original:
            if c in secret:
                new.append(ord(c))
            else:
                new.append(c)
        new = ''.join(new)
        return new

    def obfuscate_data(self, arg):
        original = arg['value']
        tpe = arg['type']
        if not tpe or not original:
            return '****'
        if tpe not in self.mapping:
            self.mapping.update({tpe: random.randint(0, 111)})

        if original in ['nil', 'true', 'false']:
            return original
        if tpe in ['str', 'uuid']:
            picked = self.obfuscate_string(original)
        elif tpe in [ "bte", "sht", "int", "lng", "hge"]:
            picked = int(original) * self.mapping[tpe]
        elif tpe in ["flt", "dbl"]:
            picked = float(original) * self.mapping[tpe]
        elif tpe in ["oid", "void"]:
            picked = original
        elif tpe in ["date", "daytime", "time", "timestamp", "timezone"]:
            picked = self.obfuscate_temporal(original, tpe)
        else:
            picked = '***'
        return picked

    def obfuscate_sql(self, original):
        # parse the SQL statement and replace sensitive components
        original = original[1:-1]
        # Mask all string literals
        p = re.compile(r'[\'\"](.*?)[\'\"]')
        picked = p.sub('***', original)

        # TODO mask all except keywords and operators to retain structure
        if DEVELOPMENT__:
            print('OBFUSCATE QUERY ', original, picked)
        return '***'
