# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""Utilities for formatting and outputting records."""


def line_formatter(dct, output_file):
    """Format a dictionary"""
    print("[", end="", file=output_file)
    for k, v in dct.items():
        print("{}".format(v), end=",\t", file=output_file)
    print("]", file=output_file)


def raw_format(obj, output_file):
    """Print the argument"""
    print(obj, file=output_file)
