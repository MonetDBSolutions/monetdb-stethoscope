# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright 1997 - July 2008 CWI, August 2008 - 2022 MonetDB B.V.

from json import loads
import pytest
from monetdb_stethoscope import transformers


@pytest.fixture
def profiler_json_objects():
    with open("./tests/data/q01_Jun2020.json") as f:
        # This cannot be simply a map because the file is closed outside of this
        # block, therefore IO will fail. Is there a way to make this work
        # lazily?
        ret = list(map(loads, f))

    return ret


@pytest.fixture
def reconstructed_statements():
    with open("./tests/data/q01_Jun2020_statements.txt") as f:
        return f.readlines()


def test_stmt_constructor(profiler_json_objects, reconstructed_statements):
    for obj, stmt in zip(profiler_json_objects, reconstructed_statements):
        assert transformers.statement_constructor(obj)['stmt'] == stmt.strip()


def test_dummy_transformer(profiler_json_objects):
    for obj in profiler_json_objects:
        assert transformers.dummy_constructor(obj)['L0'] == 'dummy value'


def test_value_obufuscate_transformer(profiler_json_objects):
    vot = transformers.ValueObfuscateTransformer()

    for obj in map(vot, profiler_json_objects):
        for var in obj.get("args", []):
            if var.get("value") and var.get("type") not in ["bit", "void"]:
                assert var["value"] == "***", "pc={}, state={}, var_index={}".format(obj["pc"], obj["state"], var.get("arg") or var.get("ret"))
