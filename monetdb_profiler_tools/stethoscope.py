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
from monetdb_profiler_tools.formatting import line_formatter, raw_formatter
from monetdb_profiler_tools.formatting import json_formatter, json_formatter_pretty
from monetdb_profiler_tools.parsing import json_parser, identity_parser
from monetdb_profiler_tools.transformers import PrerequisiteTransformer
from monetdb_profiler_tools.transformers import ValueObfuscateTransformer, statement_constructor
from monetdb_profiler_tools.transformers import dummy_constructor

LOGGER = logging.getLogger(__name__)


@click.command(context_settings=dict(
    help_option_names=["-h", "--help"]
))
@click.argument("database")
@click.option("--include-keys", "-i", "include",
              help="A comma separated list of keys. Filter out all other keys.")
@click.option("--exclude-keys", "-e", "exclude",
              help="A comma separated list of keys to exclude")
@click.option("--pipeline", "-l", "pipeline",
              type=click.Choice([
                  'raw'
              ]),
              help="Predefined pipelines. Overrides all other options.",
              default=None)
@click.option("--formatter", "-F", "fmt",
              type=click.Choice([
                  'json',
                  'json_pretty',
                  'line',
                  'raw'
              ]),
              help="json, json_pretty, or line")
@click.option("--transformer", "-t", "trn", multiple=True,
              type=click.Choice([
                  'statement',
                  'prereqs',
                  'obfuscate',
                  # 'keep_keys',
                  # 'remove_keys',
                  'dummy',
                  'identity'
              ]))
@click.option("--output", "-o", "outfile",
              default="stdout", help="Output stream")
@click.option("--username", "-u", "username",
              default="monetdb", help="The username used to connect to"
              " the database.")
@click.option("--password", "-P", prompt="Password", hide_input=True,
              help="The password used to connect to the database."
              " If this option is not specified the user will be prompted.")
@click.option("--host", "-H", "host", default="localhost",
              help="The host where the MonetDB server is running.")
@click.option("--port", "-p", "port", default=50000,
              help="The port on which the MonetDB server is listening.")
@click.option("--heartbeat", "-b", default=0,
              help="The heartbeat frequency in milliseconds.")
def stethoscope(database, include, exclude, fmt, trn, pipeline, outfile,
                username, password, host, port, heartbeat):
    """A flexible tool to manipulate MonetDB profiler streams"""

    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)

    LOGGER.debug("Input arguments")
    LOGGER.debug("  Database: %s", database)
    LOGGER.debug("  Transformer: %s", trn)
    LOGGER.debug("  Include keys: %s", include)
    LOGGER.debug("  Exclude keys: %s", exclude)
    LOGGER.debug("  Formatter: %s", fmt)
    LOGGER.debug("  Pipeline: %s", pipeline)
    LOGGER.debug("  Output file: %s", outfile)

    cnx = pymonetdb.ProfilerConnection()
    cnx.connect(database, username=username, password=password,
                heartbeat=heartbeat, hostname=host, port=port)

    if not pipeline:
        parse_operator = json_parser()
    else:
        parse_operator = identity_parser()

    transformers = list()

    stmt = False
    idx = 0
    for t in trn:
        if t == 'statement':
            stmt = True
            stmt_idx = idx
            transformers.append(statement_constructor)
        elif t == 'prereqs':
            transformers.append(PrerequisiteTransformer())
        elif t == 'dummy':
            transformers.append(dummy_constructor)
        elif t == 'obfuscate':
            transformers.append(ValueObfuscateTransformer())
            if stmt:
                # To prevent a data leak exchange the obfuscate with the
                # statement transformer.
                (transformers[stmt_idx], transformers[idx]) = (transformers[idx], transformers[stmt_idx])
        idx += 1

    LOGGER.debug("transformers len = %d", len(transformers))

    if include:
        key_filter_operator = include_filter(include.split(','))
    elif exclude:
        key_filter_operator = exclude_filter(exclude.split(','))
    else:
        key_filter_operator = identity_filter()

    if fmt == "json":
        formatter = json_formatter
    elif fmt == "json_pretty":
        formatter = json_formatter_pretty
    elif fmt == "line":
        formatter = line_formatter
    else:
        formatter = raw_formatter

    if pipeline == 'raw':
        if include:
            LOGGER.warning("Ignoring include keys because --raw was specified")
        if exclude:
            LOGGER.warning("Ignoring exclude keys because --raw was specified")
        if fmt and fmt != "json":
            LOGGER.warning("Ignoring formatter %s because --raw was specified", fmt)

        formatter = raw_formatter

    out_file = sys.stdout
    if outfile != "stdout":
        out_file = open(outfile, "w")

    while True:
        try:
            # read
            s = cnx.read_object()
            # parse
            json_object = parse_operator(s)

            # transform
            for t in transformers:
                json_object = t(json_object)
            json_object = key_filter_operator(json_object)

            # filter
            # format
            formatter(json_object, out_file)
        except pymonetdb.OperationalError as oe:
            LOGGER.error("Got an Operational Error from the database: %s", oe)
            break
        except Exception as e:
            LOGGER.warn("Failed operating on %s (%s)", json.dumps(json_object, indent=2), e)
