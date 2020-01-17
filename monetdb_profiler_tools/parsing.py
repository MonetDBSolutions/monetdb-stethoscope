# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.


import json
import logging
from monetdb_profiler_tools.utilities import identity_function

LOGGER = logging.getLogger(__name__)


def parser_wrapper(json_str):
    """JSON parser with exception logging"""
    try:
        return json.loads(json_str)
    except Exception as e:
        LOGGER.warn("Parsing failed for %s (%s)", json_str, e)
        return dict()


def json_parser():
    """Returns a callable that can parse JSON strings."""
    return parser_wrapper


def identity_parser():
    return identity_function
