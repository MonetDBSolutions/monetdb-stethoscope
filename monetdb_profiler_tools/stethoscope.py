# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""This is the implementation of stethoscope, a tool to interact with MonetDB
profiler streams."""

import json
import logging
import sys
import click
import pymonetdb
from monetdb_profiler_tools.filtering import include_filter, exclude_filter
from monetdb_profiler_tools.filtering import identity_filter
from monetdb_profiler_tools.formatting import line_formatter, raw_format

LOGGER = logging.getLogger(__name__)


@click.command()
@click.argument("database")
@click.option("--include-keys", "-i", "include",
              help="A comma separated list of keys. Filter out all other keys.")
@click.option("--exclude-keys", "-e", "exclude",
              help="A comma separated list of keys to exclude")
@click.option("--formatter", "-f", "fmt", default="raw")
@click.option("--raw", "-r", "raw", is_flag=True)
@click.option("--output", "-o", "outfile", default="stdout")
def stethoscope(database, include, exclude, fmt, raw, outfile):
    """A flexible tool to manipulate MonetDB profiler streams"""

    logging.basicConfig(level=logging.DEBUG)

    LOGGER.debug("Input arguments")
    LOGGER.debug("  Database: %s", database)
    LOGGER.debug("  Include keys: %s", include)
    LOGGER.debug("  Exclude keys: %s", exclude)
    LOGGER.debug("  Formatter: %s", fmt)
    LOGGER.debug("  Raw: %s", raw)
    LOGGER.debug("  Output file: %s", outfile)

    cnx = pymonetdb.ProfilerConnection()
    cnx.connect(database, username='monetdb', password='monetdb', heartbeat=0)

    if include:
        operator = include_filter(include.split(','))
    elif exclude:
        operator = exclude_filter(exclude.split(','))
    else:
        operator = identity_filter

    if fmt == "raw":
        formatter = raw_format
    if fmt == "line":
        formatter = line_formatter

    if raw:
        if include:
            LOGGER.warning("Ignoring include keys because --raw was specified")
        if exclude:
            LOGGER.warning("Ignoring exclude keys because --raw was specified")
        if fmt and fmt != "raw":
            LOGGER.warning("Ignoring formatter %s because --raw was specified", fmt)

        formatter = raw_format
        operator = identity_filter

    out_file = sys.stdout
    if outfile != "stdout":
        out_file = open(outfile, "w")

    while True:
        json_object = operator(json.loads(cnx.read_object()))
        formatter(json_object, out_file)
