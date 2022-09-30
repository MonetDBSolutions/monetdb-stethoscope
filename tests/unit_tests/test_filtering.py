# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright 1997 - July 2008 CWI, August 2008 - 2022 MonetDB B.V.

"""Tests for the key filtering module"""

from monetdb_stethoscope import filtering


def test_filter_keys_include():
    dct1 = {'a': 1, 'b': 2, 'c': 3, 'phase': 'mal_engine'}

    included_keys = ["a"]
    dct_filtered = filtering.filter_keys_include(dct1, included_keys)
    keys = dct_filtered.keys()
    assert "a" in keys
    assert "b" not in keys
    assert "c" not in keys
    assert len(keys) == len(included_keys)


def test_filter_keys_exclude():
    dct1 = {'a': 1, 'b': 2, 'c': 3, 'phase': 'mal_engine'}

    excluded_keys = ["a"]
    dct_filtered = filtering.filter_keys_exclude(dct1, excluded_keys)
    keys = dct_filtered
    assert "a" not in keys
    assert "b" in keys
    assert "c" in keys
    assert len(keys) == len(dct1) - len(excluded_keys)
