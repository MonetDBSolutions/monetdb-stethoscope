# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""Module that implements transformers."""

from monetdb_profiler_tools.utilities import identity_function
import json
import logging

LOGGER = logging.getLogger(__name__)


def statement_constructor(json_object):
    module = json_object.get("module")
    function = json_object.get("function")

    program = json_object.get("program")
    operator = json_object.get("operator")

    if operator is None:
        stmt = f"{module}.{function}"
    else:
        if operator == 'function':
            stmt = f'{operator} {program}()'
        else:
            stmt = f'{operator} {program}'

    default_values = {
        "int": 0,
        "str": '""'
    }

    args = ""
    rets = ""
    ret_type = ""
    ret_num = 0

    for arg in json_object.get("args", []):
        var_name = arg.get("var", "undefined")
        vtype = arg.get("type", "undefined")
        if arg.get("ret") is not None:
            if ret_num > 0:
                rets += ','
                ret_type += ','

            ret_str = f'{var_name}:{vtype}'
            ret_num += 1
            rets += ret_str
            ret_type += vtype
        else:
            value = arg.get("value")
            count = arg.get("count")
            default = default_values.get(vtype, "unknown")
            const = bool(arg.get("const", False))

            if arg.get("arg", 0) > ret_num:
                args += ','

            if const:
                arg_str = f"{value}:{vtype}"
            elif value is not None:
                arg_str = f"{var_name}={value}:{vtype}"
            elif count is None:
                arg_str = f"{var_name}={default}:{vtype}"
            else:
                arg_str = f"{var_name}=[{count}]:{vtype}"
            args += arg_str

    if  operator is not None:
        statement = f'{stmt}'
        if operator == 'function':
            if ret_num == 1:
                statement += f":{ret_type};"
            elif ret_num > 1:
                statement += f":({ret_type});"
            else:
                statement += ';'
    elif ret_num == 0:
        statement = f'{stmt}({args});'
    elif ret_num == 1:
        statement = f'{rets} := {stmt}({args});'
    else:
        statement = f'({rets}) := {stmt}({args});'

    rdict = dict(json_object)
    rdict['stmt'] = statement
    return rdict


def statement_transformer():
    return statement_constructor


def dummy_transformer():
    return dummy_constructor


def dummy_constructor(json_object):
    cnt = 0
    keys = json_object.keys()
    while f'L{cnt}' in keys:
        cnt += 1

    rdict = dict(json_object)
    rdict[f'L{cnt}'] = 'dummy value'

    return rdict


def identity_transformer():
    return identity_function


class PrerequisiteTransformer:
    def __init__(self):
        self._var_to_pc = dict()
        self._resolved_prereqs = dict()

    def __call__(self, json_object):
        state = json_object.get('state', 'NA')

        if state == 'done':
            pc = json_object.get('pc')
            rdict = dict(json_object)
            rdict['prereq'] = self._resolved_prereqs.get(pc, [])
            return rdict
        elif state != 'start':
            return json_object

        # Ignore function and end operators
        ignore_ops = ['function', 'end']

        op = json_object.get('operator')
        if op and op in ignore_ops:
            return json_object

        self.install_return_values(json_object)
        return self.find_prerequisites(json_object)

    def lookup(self, variable):
        pc = self._var_to_pc.get(variable)
        if pc is None:
            LOGGER.debug("Variable %s not found in lookup table", variable)

        return pc

    def install(self, variable, pc):
        if variable in self._var_to_pc:
            LOGGER.warn("Variable %s already in lookup table: pc=%d",
                        variable,
                        self._var_to_pc[variable])
            LOGGER.warn("This will produce incorrect prerequisites!")
        self._var_to_pc[variable] = pc

    def install_return_values(self, json_object):
        for v in json_object.get('args', []):
            # No more return values
            if v.get("ret") is None:
                break

            pc = json_object.get("pc")
            vname = v.get("var")

            if pc and vname:
                self.install(vname, pc)
            else:
                LOGGER.warn("pc or return variable undefined in %s", json_object)
                LOGGER.warn("Ignoring")
                return

    def find_prerequisites(self, json_object):
        rdict = dict(json_object)
        prereqs = list()

        for v in json_object.get("args", []):
            # no need to handle return values and constants
            if v.get("ret") or v.get('const') == 1:
                continue

            var = v.get("var")
            pc = self._var_to_pc.get(var)
            if pc:
                prereqs.append(pc)
            else:
                LOGGER.warn("Variable %s not in lookup table: %s",
                            var,
                            json.dumps(json_object, indent=2))

        if prereqs:
            pc = json_object.get('pc')
            self._resolved_prereqs[pc] = prereqs
            rdict["prereq"] = prereqs

        return rdict
