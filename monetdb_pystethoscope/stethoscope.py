# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""This is the implementation of stethoscope, a tool to interact with MonetDB
profiler streams."""

import json
import sys
import argparse
from monetdb_pystethoscope import __version__
from monetdb_pystethoscope.api import *


def stethoscope(args):
    """A flexible tool to manipulate MonetDB profiler streams"""

    cnx = StethoscopeProfilerConnection()
    cnx.connect(args.database, username=args.username, password=args.password,
                hostname=args.hostname, port=args.port, heartbeat=0)

    print("Connected to the database: {}".format(args.database), file=sys.stderr)

    if not args.pipeline:
        parse_operator = json_parser()
    else:
        parse_operator = identity_parser()

    transformers = list()

    stmt = False
    idx = 0
    for t in args.transformer:
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

    if args.include_keys:
        key_filter_operator = include_filter(args.include_keys)
    elif args.exclude_keys:
        key_filter_operator = exclude_filter(args.exclude_keys)
    else:
        key_filter_operator = identity_filter()

    if args.formatter == "json":
        formatter = json_formatter
    elif args.formatter == "json_pretty":
        formatter = json_formatter_pretty
    elif args.formatter == "line":
        formatter = line_formatter
    else:
        formatter = raw_formatter

    if args.pipeline == 'raw':
        if args.include or args.exclude:
            print("Ignoring key filter operation because --raw was specified", file=sys.stderr)
        if args.formatter:
            print("Ignoring formatter because --raw was specified", file=sys.stderr)
        if transformers:
            print("Ignoring transformers because --raw was specified", file=sys.stderr)

        transformers = list()
        key_filter_operator = identity_filter()
        formatter = raw_formatter

    out_file = sys.stdout
    if args.output != "stdout":
        out_file = open(args.output, "w")

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
        except OperationalError as oe:
            print("Got an Operational Error from the database: {}".format(oe),
                  file=sys.stderr)
            break
        except Exception as e:
            print("Failed operating on {} ({})"
                  .format(
                      json.dumps(json_object, indent=2),
                      e),
                  file=sys.stderr)


def main():
    desc = "MonetDB profiling tool\n{} version {}".format(sys.argv[0], __version__)
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('database', help='The database to connect to')
    parser.add_argument('-i', '--include-keys', nargs='*',
                        help='A list of keys to keep.')
    parser.add_argument('-e', '--exclude-keys', nargs='*',
                        help='A list of keys to exclude.')
    parser.add_argument('-l', '--pipeline', choices=['raw'],
                        help='Predefined pipelines. Overrides all other options.')
    parser.add_argument('-F', '--formatter',
                        choices=[
                            'json',
                            'json_pretty',
                            'line',
                            'raw'
                        ], help='The formatter used to display the values.')
    parser.add_argument('-t', '--transformer', nargs='*',
                        choices=[
                            'statement',
                            'prereqs',
                            'obfuscate',
                            'dummy',
                            'identity'
                        ],
                        help="foo")
    parser.add_argument('-o', '--output', default="stdout", help="Output stream")
    parser.add_argument('-u', '--username', default="monetdb",
                        help="The username used to connect to the database")
    parser.add_argument('-H', '--hostname', default="localhost",
                        help="The hostname used to connect to the database")
    parser.add_argument('-P', '--password', default="monetdb",
                        help="The password used to connect to the database")
    parser.add_argument('-p', '--port', default=50000,
                        help="The port on which the MonetDB server is listening.")

    arguments = parser.parse_args()
    stethoscope(arguments)


if __name__ == '__main__':
    main()
