# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""Utilities for formatting and outputting records."""

import io
import json


def line_formatter(dct):
    """Formats a dictionary `dct` into one line and prints it to the
`output_stream`.

Values in `dct` are written one after the other, separated by the string
',\\t'. The whole line is surrounded by square brackets."""

    output = io.StringIO()
    print("[", end="", file=output)
    first = True
    for v in dct.values():
        if first:
            print("{}".format(v), end="", file=output)
            first = False
        else:
            print(",\t{}".format(v), end="", file=output)
    print("]", end="", file=output)

    return output.getvalue()


def raw_formatter(obj):
    """Prints the argument `obj` argument to the `output_stream` without further
formatting."""
    return obj


def json_formatter(dct):
    """Creates a JSON string from the given dictionary (`dct`) and prints it to the
given `output_stream`."""
    return json.dumps(dct)


def json_formatter_pretty(dct):
    return json.dumps(dct, indent=2)
