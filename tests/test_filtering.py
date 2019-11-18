"""Tests for the filtering module"""

from monetdb_profiler_tools import filtering


def test_filter_keys_include():
    dct1 = {'a': 1, 'b': 2, 'c': 3}

    included_keys = ["a"]
    dct_filtered = filtering.filter_keys_include(dct1, included_keys)
    keys = dct_filtered.keys()
    assert "a" in keys
    assert "b" not in keys
    assert "c" not in keys
    assert len(keys) == len(included_keys)


def test_filter_keys_exclude():
    dct1 = {'a': 1, 'b': 2, 'c': 3}

    excluded_keys = ["a"]
    dct_filtered = filtering.filter_keys_exclude(dct1, excluded_keys)
    keys = dct_filtered
    assert "a" not in keys
    assert "b" in keys
    assert "c" in keys
    assert len(keys) == len(dct1) - len(excluded_keys)
