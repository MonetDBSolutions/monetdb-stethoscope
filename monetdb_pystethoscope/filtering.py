# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"Tools useful for filtering JSON objects based on keys."

import sys
from monetdb_pystethoscope.utilities import identity_function

# Filtering operators: Given one a list of keys return an operator that takes a
# dictionary and returns a filtered version of it. We also include the identity
# operator if we need no filtering at all.


def include_filter(included_keys):
    """Returns a filter that only keeps the keys in `included_keys` list."""
    return lambda x: filter_keys_include(x, included_keys)


def exclude_filter(excluded_keys):
    """Returns a filter that discards the keys in `excluded_keys` list."""
    return lambda x: filter_keys_exclude(x, excluded_keys)


def identity_filter():
    """Returns a filter that does nothing."""
    return identity_function


def filter_keys_include(json_object, included_keys):
    """Create a new dictionary object by filtering a single given dictionary object
including the keys specified in the iterable `included_keys`.

    """

    ret = {k: v for (k, v) in json_object.items() if k in included_keys}
    for i in included_keys:
        if i not in ret:
            print("Key {} not found in the JSON object".format(i),
                  file=sys.stderr)
    return ret


def filter_keys_exclude(json_object, excluded_keys):
    """Create a new dictionary by filtering a single given dictionary excluding the
keys specified in the iterable `excluded_keys`.

    """
    # We do not need to log anything here, since we are excluding keys
    return {k: v for (k, v) in json_object.items() if k not in excluded_keys}
