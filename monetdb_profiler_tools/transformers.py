# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""Module that implements transformers."""

import logging

LOGGER = logging.getLogger(__name__)


def statement_reconstructor(json_object):
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
            value = arg.get("value", None)
            count = arg.get("count", None)
            default = default_values.get(vtype, "unknown")
            const = bool(arg.get("const", False))

            if arg.get("arg") > ret_num:
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
