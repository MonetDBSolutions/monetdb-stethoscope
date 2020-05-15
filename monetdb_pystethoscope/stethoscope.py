# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""This is the implementation of stethoscope, a tool to interact with MonetDB
profiler streams."""

import json
import sys
import click
import pymonetdb
from monetdb_pystethoscope.filtering import include_filter, exclude_filter
from monetdb_pystethoscope.filtering import identity_filter
from monetdb_pystethoscope.formatting import line_formatter, raw_formatter
from monetdb_pystethoscope.formatting import json_formatter, json_formatter_pretty
from monetdb_pystethoscope.parsing import json_parser, identity_parser
from monetdb_pystethoscope.transformers import PrerequisiteTransformer
from monetdb_pystethoscope.transformers import ValueObfuscateTransformer, statement_constructor
from monetdb_pystethoscope.transformers import dummy_constructor


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
@click.version_option(message="MonetDB profiling tool\n%(prog)s, version %(version)s")
def stethoscope(database, include, exclude, fmt, trn, pipeline, outfile,
                username, password, host, port):
    """A flexible tool to manipulate MonetDB profiler streams"""

    cnx = pymonetdb.ProfilerConnection()
    cnx.connect(database, username=username, password=password,
                hostname=host, port=port, heartbeat=0)

    print(f"Connected to the database: {database}", file=sys.stderr)

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
        if include or exclude:
            print("Ignoring key filter operation because --raw was specified", file=sys.stderr)
        if fmt:
            print("Ignoring formatter because --raw was specified", file=sys.stderr)
        if transformers:
            print("Ignoring transformers because --raw was specified", file=sys.stderr)

        transformers = list()
        key_filter_operator = identity_filter()
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
            print(f"Got an Operational Error from the database: {oe}", file=sys.stderr)
            break
        except Exception as e:
            bad_obj = json.dumps(json_object, indent=2)
            print(f"Failed operating on {bad_obj} ({e})", file=sys.stderr)
