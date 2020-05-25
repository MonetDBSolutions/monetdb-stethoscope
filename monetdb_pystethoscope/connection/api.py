# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

"""A small API that implements the connection to the Profiler"""

# NOTE: This module MUST be moved to pymonetdb

# import logging
from pymonetdb import mapi
from pymonetdb.exceptions import OperationalError, ProgrammingError

# LOGGER = logging.getLogger(__name__)


class StethoscopeProfilerConnection(object):
    """
    A connection to the MonetDB profiler.
    """

    def __init__(self):
        self._mapi = mapi.Connection()
        self._heartbeat = 0
        self._buffer = ""
        self._objects = list()

    def _command(self, operation):
        if self._mapi.state != mapi.STATE_READY:
            raise (ProgrammingError, "Not connected")
        self._mapi._putblock(operation)

    def _response(self):
        r = self._mapi._getblock()

        if not r or len(r) == 0:
            pass # nothing to do
        elif r.startswith("{") and len(self._buffer) == 0:
            self._buffer = r
        else:
            raise OperationalError("bad response when connecting to the profiler: %s" % r)

    def connect(self, database, username="monetdb", password="monetdb", hostname=None, port=50000, heartbeat=0):
        self._heartbeat = heartbeat
        self._mapi.connect(database, username, password, "mal", hostname, port)
        self._command("profiler.setheartbeat(%d);\n" % heartbeat)
        self._response()
        try:
            self._command("profiler.openstream();\n")
            self._response()
        except OperationalError as e:
            # We might be talking to an older version of MonetDB. Try connecting
            # the old way.
            # LOGGER.warning("Connection failed. Attempting to connect using the old API.")
            self._command("profiler.openstream(3);\n")
            self._response()

    def read_object(self):
        if len(self._buffer) == 0:
            self._buffer = self._mapi._getblock()
        while not self._buffer.endswith("}\n"):
            self._buffer += self._mapi._getblock()

        r = self._buffer[:-1]
        self._buffer = ""
        return r
