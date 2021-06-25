# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""Tools for changing (adding information) the profiler objects."""

import json
import logging
import sys


LOGGER = logging.getLogger(__name__)


def statement_constructor(json_object):
    """Reconstruct a MAL statement from the given profiler object."""

    module = json_object.get("module")
    function = json_object.get("function")

    program = json_object.get("program")
    operator = json_object.get("operator")

    if operator is None:
        stmt = "{}.{}".format(module, function)
    else:
        if operator == 'function':
            stmt = '{} {}()'.format(operator, program)
        else:
            stmt = '{} {}'.format(operator, program)

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

            ret_str = "{}:{}".format(var_name, vtype)
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
                arg_str = "{}".format(value)
            elif value is not None:
                arg_str = "{}={}".format(var_name, value)
            elif count is None:
                arg_str = "{}={}".format(var_name, default)
            else:
                arg_str = "{}=[{}]".format(var_name, count)
            args += arg_str

    if operator is not None:
        statement = stmt
        if operator == 'function':
            if ret_num == 1:
                statement += ":{};".format(ret_type)
            elif ret_num > 1:
                statement += ":({});".format(ret_type)
            else:
                statement += ';'
    elif ret_num == 0:
        statement = "{}({});".format(stmt, args)
    elif ret_num == 1:
        statement = "{} := {}({});".format(rets, stmt, args)
    else:
        statement = "({}) := {}({});".format(rets, stmt, args)

    rdict = dict(json_object)
    rdict['stmt'] = statement
    return rdict


def dummy_constructor(json_object):
    cnt = 0
    keys = json_object.keys()
    while 'L{}'.format(cnt) in keys:
        cnt += 1

    rdict = dict(json_object)
    rdict['L{}'.format(cnt)] = 'dummy value'

    return rdict


class PrerequisiteTransformer:
    """Add a list of PCs of prerequisite instructions."""

    def __init__(self):
        self._var_to_pc = dict()
        self._resolved_prereqs = dict()
        self._ignore_ops = ['function', 'end']

    def __call__(self, json_object):
        state = json_object.get('state', 'NA')
        rdict = dict(json_object)

        if state == 'done':
            pc = json_object.get('pc')
            rdict['prereq'] = self._resolved_prereqs.get(pc, [])
            return rdict
        elif state == 'start':
            pc = json_object.get('pc', -1)
            if pc == 0:
                # Reset symbol table at the start of a query (pc==0 &&
                # state=='start').
                self._var_to_pc = dict()
                self._resolved_prereqs = dict()
                rdict['prereq'] = list()
                return rdict
        else:
            LOGGER.error("PrerequisiteTransformer cannot handle state %s", state)
            return json_object

        op = json_object.get('operator')
        if op and op in self._ignore_ops:
            rdict['prereq'] = list()
            return rdict

        self.install_return_values(json_object)
        return self.find_prerequisites(json_object)

    def lookup(self, variable):
        pc = self._var_to_pc.get(variable)
        if pc is None:
            LOGGER.error("Variable %s not found in lookup table", variable)

        return pc

    def install(self, variable, pc):
        if variable in self._var_to_pc:
            LOGGER.error("Variable %s already in lookup table: pc=%s", variable, self._var_to_pc[variable])
            LOGGER.error("This will produce incorrect prerequisites!")
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
                LOGGER.error("pc or return variable undefined in %s", json_object)
                LOGGER.error("Ignoring", file=sys.stderr)
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
                LOGGER.error("Variable %s not in lookup table: %s", var, json.dumps(json_object, indent=2))

        if prereqs:
            pc = json_object.get('pc')
            self._resolved_prereqs[pc] = prereqs
        rdict["prereq"] = prereqs

        return rdict


class ValueObfuscateTransformer:
    """Replace every literal value in the plan with three asterisks."""

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

    def __call__(self, json_object):
        rdict = dict(json_object)
        for var in rdict.get("args", []):
            if var.get("type", "void") in self._types and var.get("value", None):
                var["value"] = "***"

        return rdict
