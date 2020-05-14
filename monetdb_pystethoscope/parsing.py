# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.


import json
import sys
from monetdb_pystethoscope.utilities import identity_function


def parser_wrapper(json_str):
    """JSON parser with exception logging"""
    try:
        return json.loads(json_str)
    except Exception as e:
        print(f"Parsing failed for {json_str} ({e})", file=sys.stderr)
        return dict()


def json_parser():
    """Returns a callable that can parse JSON strings."""
    return parser_wrapper


def identity_parser():
    return identity_function
