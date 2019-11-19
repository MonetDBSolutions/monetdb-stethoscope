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
    """Format a dictionary"""
    print("[", end="")
    for k, v in dct.items():
        print("{}".format(v), end=",\t")
    print("]")


def raw_format(obj):
    """Print the argument"""
    print(obj)


def include_op(included_keys):
    """Return a filter that only keeps the keys in `included_keys`."""
    return lambda x: ftools.filter_keys_include(x, included_keys)


def exclude_op(excluded_keys):
    """Return a filter that discards the keys in `excluded_keys`."""
    return lambda x: ftools.filter_keys_exclude(x, excluded_keys)


def identity_op(input_object):
    """Return the argument as is."""
    return input_object


@click.command()
@click.argument("database")
@click.option("--include-keys", "-i", "include")
@click.option("--exclude-keys", "-e", "exclude")
@click.option("--raw", "-r", "raw", is_flag=True)
def stethoscope(database, include, exclude, raw):
    """foo"""
    print(include)
    print(exclude)
    cnx = pymonetdb.ProfilerConnection()
    cnx.connect(database, username='monetdb', password='monetdb', heartbeat=0)
    formatter = format_object

    if include:
        operator = include_op(include.split(','))
    elif exclude:
        operator = exclude_op(exclude.split(','))
    else:
        operator = identity_op

    if raw:
        formatter = raw_format

    while True:
        json_object = operator(json.loads(cnx.read_object()))
        formatter(json_object)
