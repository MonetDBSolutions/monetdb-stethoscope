# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""Module that implements transformers."""

import logging

LOGGER = logging.getLogger(__name__)


def statement_reconstructor(json_object):
    stmt = "{}.{}".format(json_object.get("module"),
                          json_object.get("function"))

    args = ""
    rets = ""
    ret_num = 0
    for arg in json_object.get("args", []):
        if arg.get("ret") is not None:
            if ret_num > 0:
                ret_str = ','
            ret_str = '{}:{}'.format(
                arg.get("var"),
                arg.get("type")
            )
            ret_num += 1
            rets += ret_str
        else:
            if arg.get("arg") > ret_num:
                args += ','
            arg_str = "{}=[{}]:{}".format(
                arg.get("var"),
                arg.get("count"),
                arg.get("type")
            )
            args += arg_str

    statement = '{} := {}({})'.format(
        rets,
        stmt,
        args
    )

    json_object['stmt_rec'] = statement
    return json_object
