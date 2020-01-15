# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""Utilities for formatting and outputting records."""

import json


def line_formatter(dct, output_stream):
    """Formats a dictionary `dct` into one line and prints it to the
`output_stream`.

Values in `dct` are written one after the other, separated by the string
',\\t'. The whole line is surrounded by square brackets."""
    print("[", end="", file=output_stream)
    first = True
    for k, v in dct.items():
        if first:
            print("{}".format(v), end="", file=output_stream)
            first = False
        else:
            print(",\t{}".format(v), end="", file=output_stream)
    print("]", file=output_stream)


def raw_formatter(obj, output_stream):
    """Prints the argument `obj` argument to the `output_stream` without further
formatting."""
    print(obj, file=output_stream)


def json_formatter(dct, output_stream):
    """Creates a JSON string from the given dictionary (`dct`) and prints it to the
given `output_stream`."""
    print(json.dumps(dct), file=output_stream)
