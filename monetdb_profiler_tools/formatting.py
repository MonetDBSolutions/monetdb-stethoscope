# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""Utilities for formatting and outputting records."""


def line_formatter(dct):
    """Format a dictionary"""
    print("[", end="")
    for k, v in dct.items():
        print("{}".format(v), end=",\t")
    print("]")


def raw_format(obj):
    """Print the argument"""
    print(obj)
