# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""This is the implementation of stethoscope, a tool to interact with MonetDB
profiler streams."""

import json
import click
import pymonetdb
import monetdb_profiler_tools.filtering as ftools


def format_object(dct):
    """Format an object"""
    print("[", end="")
    for k, v in dct.items():
        print("{}".format(v), end=",\t")
    print("]")


def include_op(included_keys):
    return lambda x: ftools.filter_keys_include(x, included_keys)


def exclude_op(excluded_keys):
    return lambda x: ftools.filter_keys_exclude(x, excluded_keys)


@click.command()
@click.argument("database")
@click.option("--include-keys", "-i", "include")
@click.option("--exclude-keys", "-e", "exclude")
def stethoscope(database, include, exclude):
    """foo"""
    print(include)
    print(exclude)
    cnx = pymonetdb.ProfilerConnection()
    cnx.connect(database, username='monetdb', password='monetdb', heartbeat=0)

    if include:
        includes = include.split(',')
        operator = include_op(includes)
    elif exclude:
        excludes = exclude.split(',')
        operator = exclude_op(excludes)
    else:
        operator = id

    while True:
        json_object = operator(json.loads(cnx.read_object()))
        format_object(json_object)
