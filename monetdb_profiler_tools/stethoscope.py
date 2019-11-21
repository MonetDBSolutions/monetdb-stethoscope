# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""This is the implementation of stethoscope, a tool to interact with MonetDB
profiler streams."""

import json
import click
import pymonetdb
from monetdb_profiler_tools.filtering import include_filter, exclude_filter
from monetdb_profiler_tools.filtering import identity_filter
from monetdb_profiler_tools.formatting import line_formatter, raw_format


@click.command()
@click.argument("database")
@click.option("--include-keys", "-i", "include",
              help="A comma separated list of keys. Filter out all other keys.")
@click.option("--exclude-keys", "-e", "exclude",
              help="A comma separated list of keys to exclude")
@click.option("--formatter", "-f", "fmt", default="line")
@click.option("--raw", "-r", "raw", is_flag=True)
def stethoscope(database, include, exclude, fmt, raw):
    """A flexible tool to manipulate MonetDB profiler streams"""
    print(include)
    print(exclude)
    cnx = pymonetdb.ProfilerConnection()
    cnx.connect(database, username='monetdb', password='monetdb', heartbeat=0)

    if include:
        operator = include_filter(include.split(','))
    elif exclude:
        operator = exclude_filter(exclude.split(','))
    else:
        operator = identity_filter

    if fmt == "line":
        formatter = line_formatter

    if raw:
        if include or exclude or fmt:
            # TODO: log a warning about incompatible options
            pass
        formatter = raw_format
        operator = identity_filter

    while True:
        json_object = operator(json.loads(cnx.read_object()))
        formatter(json_object)
