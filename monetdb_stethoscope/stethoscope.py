# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""This is the implementation of stethoscope, a tool to interact with MonetDB
profiler streams."""

import argparse
import json
import logging
import logging.config
import signal
import sys

from monetdb_stethoscope import __version__
import monetdb_stethoscope.api as api
from monetdb_stethoscope import DEVELOPMENT__

LOGGER = logging.getLogger(__name__)


def stethoscope(args):
    """A flexible tool to manipulate MonetDB profiler streams"""

    inputfile = None
    if args.input:
        try:
            inputfile = open(args.input, "r")
        except IOError as msg:
            LOGGER.error("Could not open '%s':%s", args.input, msg)
            exit(1)
    if not inputfile:
        cnx = api.StethoscopeProfilerConnection()
        cnx.connect(args.database, username=args.username, password=args.password,
                    hostname=args.hostname, port=args.port, heartbeat=0)
        # Do not use the logger here. The user needs to see this.
        LOGGER.info("Connected to database: %s", args.database)
    else:
        cnx = None

    if not args.pipeline:
        parse_operator = api.json_parser()
    else:
        parse_operator = api.identity_parser()

    transformers = list()

    stmt = False
    prereqs = False
    idx = 0
    stmt_idx = 0
    for t in args.transformer:
        if t == 'statement':
            stmt = True
            stmt_idx = idx
            transformers.append(api.statement_constructor)
        elif t == 'prereqs':
            transformers.append(api.PrerequisiteTransformer())
            prereqs = True
        elif t == 'dummy':
            transformers.append(api.dummy_constructor)
        elif t == 'identity':
            # Do nothing
            continue
        elif t == 'mask':
            transformers.append(api.ValueObfuscateTransformer())
            if stmt:
                # To prevent a data leak exchange the obfuscate with the
                # statement transformer.
                (transformers[stmt_idx], transformers[idx]) = (transformers[idx], transformers[stmt_idx])
        elif t == 'obfuscate':
            transformers.append(api.ObfuscateTransformer())
            if stmt:
                (transformers[stmt_idx], transformers[idx]) = (transformers[idx], transformers[stmt_idx])
        else:
            LOGGER.warning("Unknown transformer %s. Ignoring.", t)
            continue
        idx += 1

    if args.include_keys:
        if stmt:
            args.include_keys.append("stmt")
        if prereqs:
            args.include_keys.append("prereq")
        key_filter_operator = api.include_filter(args.include_keys)
    elif args.exclude_keys:
        key_filter_operator = api.exclude_filter(args.exclude_keys)
    else:
        key_filter_operator = api.identity_filter()

    if args.formatter == "json":
        formatter = api.json_formatter
    elif args.formatter == "json_pretty":
        formatter = api.json_formatter_pretty
    elif args.formatter == "line":
        formatter = api.line_formatter
    else:
        formatter = api.raw_formatter

    if args.pipeline == 'raw':
        if args.include_keys or args.exclude_keys:
            LOGGER.warning("Ignoring key filter operation because --raw was specified")
        if args.formatter:
            LOGGER.warning("Ignoring formatter because --raw was specified")
        if transformers:
            LOGGER.warning("Ignoring transformers because --raw was specified")

        transformers = list()
        key_filter_operator = api.identity_filter()
        formatter = api.raw_formatter

    out_file = sys.stdout
    if args.output != "stdout":
        out_file = open(args.output, "w")

    s = ""
    while True:
        try:
            # Read line from source. If an error happens while reading input
            # bail out.
            if inputfile:
                s = inputfile.readline()
                if not s:
                    break
            elif cnx is not None:
                s = cnx.read_object()
            else:
                LOGGER.error("Invalid connection AND input file. How did this happen?")
                break

            # Ignore empty lines
            if len(s) == 0:
                continue

            # Parse line as a JSON object
            json_object = parse_operator(s)

            # Apply transformers to JSON object
            for t in transformers:
                json_object = t(json_object)
            # Filter out keys (include/exclude key filters)
            json_object = key_filter_operator(json_object)

            # filter objects
            # Not Implemented yet

            # format
            print(formatter(json_object), file=out_file,
                  flush=args.flush)

            # A  limitation of the current profiler is that it only emits the
            # start/done events of the first statement in a barrier (dataflow) block
            # A hack is to recognize the 'done' event of a barrier block
            # and also emit an exit statement, placing it at pc = lastpc + 1
            # json_object['pc] = lastpc + 1
            # json_object['barrier'] = 'exit'
            # json_object['args']=  copy['args'][:2]
            # json_object['fcnname'] = ''
            # json_object['modname'] = ''
            # json_object['state'] = 'start'
            # print(formatter(copy), file=out_file)
            # json_object['state'] = 'done'
            # print(formatter(copy), file=out_file)
            # if 'pc' in json_object:
            #    lastpc = json_object['pc']

        except IOError as ioe:
            LOGGER.error("IO error %s while reading from file", ioe)
            break
        except api.OperationalError as oe:
            LOGGER.error("Got an Operational Error from the database: %s", oe)
            break
        except json.JSONDecodeError as pe:
            # Could not parse json object. Inform the user, taking care not to
            # leak data we should not, and continue with the next object in the
            # stream.
            msg = s
            if ("obfuscate" in args.transformer or "mask" in args.transformer) and not DEVELOPMENT__:
                msg = "***"
            LOGGER.error("Parse error while parsing %s (%s)", msg, pe)
            if DEVELOPMENT__:
                raise
        except KeyboardInterrupt:
            # Do not log, notify user.
            LOGGER.info("Received a keyboard interupt. Shutting down...")
            break
        except Exception as e:
            # An exception that we did not account for happened. Instead of
            # crashing report it to the user, taking care not leak data we
            # should not, and attempt to continue the execution. In the worst
            # case we will fail for the rest of the stream.
            msg = s
            if ("obfuscate" in args.transformer or "mask" in args.transformer) and not DEVELOPMENT__:
                msg = "***"
            LOGGER.error("Failed operating on %s (%s)", msg, e)
            # Actually if we are in development do crash.
            if DEVELOPMENT__:
                raise

class NvFilter(logging.Filter):
    """A filter to show each warning only once"""
    def __init__(self):
        self.already_shown = set()

    def filter(self, record):
        ret = True
        rid = record.__dict__.get("id")
        if rid is not None:
            ret = not rid in self.already_shown
            self.already_shown.add(rid)

        return ret

def logging_configuration(args):
    logger_configuration = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'non-verbose-filter': {
                '()': NvFilter,

            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'precise',
                'filters': []
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'stethoscope.log',
                'maxBytes': 10 * 1024 * 1024,
                'backupCount': 3,
                'formatter': 'precise',
                'filters': []
            },
            'null': {
                'class': 'logging.NullHandler',
            },
        },
        'formatters': {
            'precise': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        },
        'root': {
            'handlers': ['console', 'null'],
            'level': 'WARNING',
        },
    }

    logger_configuration['root']['level'] = args.log_level.upper()
    if args.log_file:
        logger_configuration['root']['handlers'].append('file')
        logger_configuration['handlers']['file']['filename'] = args.log_file

    if args.no_console:
        logger_configuration['root']['handlers'].remove('console')

    if not args.verbose:
        logger_configuration['handlers']['console']['filters'].append('non-verbose-filter')


    logging.config.dictConfig(logger_configuration)


def sigterm_handler(snum, frame):
    LOGGER.info("Caught term signal. Exiting.")
    exit(0)


def main():
    signal.signal(signal.SIGTERM, sigterm_handler)
    desc = "MonetDB profiling tool\n{} version {}".format(sys.argv[0], __version__)
    parser = argparse.ArgumentParser(description=desc)
    input_options = parser.add_mutually_exclusive_group(required=True)
    input_options.add_argument('-d', '--database',
                               type=str,
                               help='The database to connect to')
    input_options.add_argument('-I', '--input',
                               type=str,
                               help="Read previously recorded stream")
    parser.add_argument('-i', '--include-keys', nargs='+',
                        help='A space separated list of keys to keep.')
    parser.add_argument('-e', '--exclude-keys', nargs='+',
                        help='A space separated list of keys to exclude.')
    parser.add_argument('-l', '--pipeline', choices=['raw'],
                        help='Predefined pipelines. Overrides all other options.')
    parser.add_argument('-F', '--formatter',
                        choices=[
                            'json',
                            'json_pretty',
                            'line',
                            'raw'
                        ],
                        default='json',
                        help='The formatter used to display the values.')
    parser.add_argument('-t', '--transformer', nargs='+',
                        choices=[
                            'statement',
                            'prereqs',
                            'mask',
                            'obfuscate',
                            'dummy',
                            'identity'
                        ],
                        default=[],
                        help="The transformers to add to the pipeline")
    parser.add_argument('-o', '--output', default="stdout", help="Output stream")
    parser.add_argument('-u', '--username', default="monetdb",
                        help="The username used to connect to the database")
    parser.add_argument('-H', '--hostname', default="localhost",
                        help="The hostname used to connect to the database")
    parser.add_argument('-P', '--password', default="monetdb",
                        help="The password used to connect to the database")
    parser.add_argument('-p', '--port', default=50000, type=int,
                        help="The port on which the MonetDB server is listening.")
    parser.add_argument('-V', '--verbose', action='store_true',
                        help='Show more warnings/error messages')
    parser.add_argument('-L', '--log-level',
                        choices=[
                            'debug',
                            'info',
                            'warning',
                            'error',
                            'critical',
                        ], default='info',
                        help='The logging level')
    parser.add_argument('-C', '--no-console', action='store_true', default=False,
                        help='Do not log errors and warnings to the console.')
    parser.add_argument('-O', '--log-file', help='The file where logging output will be written.')
    parser.add_argument('-U', '--flush', action='store_true',
                        help='Flush immediatelly to the output stream.')
    parser.add_argument('-v', '--version', action='version', version=desc)

    arguments = parser.parse_args()
    logging_configuration(arguments)

    stethoscope(arguments)


if __name__ == '__main__':
    main()
