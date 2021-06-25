All notable changes to this project will be documented in this file.

The format is based on `Keep a
Changelog <https://keepachangelog.com/en/1.0.0/>`__, and this project
adheres to `Semantic
Versioning <https://semver.org/spec/v2.0.0.html>`__.

`Unreleased`_
=============

`0.4.0`_ - 2021-06-25
=====================
Added
-----
- A ``--version`` option.
- Switches for controlling logging: ``--verbose``, ``--no-console``
  and ``--log-file``.
- Support for Python 3.9.

Removed
-------
- Support for Python 3.5.

Fixed
-----
- The options ``--transformer (-t)``, ``--include-keys (-i)`` and
  ``--exclude-keys (-e)`` now require at least one argument, emitting
  an error if one is not provided.
- A number of documentation bugs.
- A bug in the statement transformer that rendered statements
  erroneously.
- A bug in the the prerequisite transformer that would prevent the
  computation of prerequisites for subsequent queries after the
  first.

Changed
-------
- The name of the executable string from ``pystethoscope`` to
  ``stethoscope``.
- Made the usage string more clear about arguments to
  ``--include-keys`` and ``--exclude-keys`` being a space separated
  list and added a suggestion if a key is not found while containing
  the comma character.
- Specifying the transformers ``statement`` or ``prereqs`` adds the
  corresponding keys to the included keys list.
- Errors and warnings are now reported using the ``logging`` package from the
  python standard library.
- The name of the python package from ``monetdb_pystethoscope`` to
  ``monetdb_stethoscope``.

`0.3.2`_ - 2021-04-26
=====================
Fixed
-----
- A type mismatch with pymonetdb when connecting to a non-default
  port.

`0.3.1`_ - 2020-10-23
=====================
Changed
-------
- Added functionality to the new obfuscation method.

`0.3.0`_ - 2020-09-30
=====================
Added
-----
- A github workflow to upload automatically to PyPI on tagging.
- Help string and default value (``[]``) for the ``transformers`` option.
- Help string and default value (``raw``) for the ``formatter`` option.
- The option to provide input from a file (``-I``) or to connect to a database
  (``-d``).
- A new obfuscation method (``--transformer obfuscate``). The old method has
  been renamed to mask: ``--transformer mask``.
- A boolean that distinguishes between development and production modes. In
  development certain exceptions get propagated.
- Rudimentary handling for SIGINT: A friendlier message is shown.

Fixed
-----
- A reference to non existing arguments that prevented startup (#18).
- A data leak under the obfuscation transformer when exceptions happened.
- A data leak under the obfuscation transformer of UUIDs.

Changed
-------
- Formatters now return strings instead of printing them. Printing happens on
  the main loop.
- The JSON formatter is now the default.

`0.2.0`_ - 2020-07-22
=====================
Added
-----
- ``monetdb_pystethoscope.api`` module that gathers all the public API.
- The docstrings to the documentation.

Removed
-------
- Dependency on click.

`0.1.3`_ - 2020-05-25
=====================
Fixed
-----
- A bug in the statement constructor (`#13
  <https://github.com/MonetDBSolutions/monetdb-pystethoscope/issues/13>`__)

Added
-----
- An API for connecting to the MonetDB server profiler.
  This should be backported to pymonetdb in the future.
- Some more tests
- Coverage reports

`0.1.2`_ - 2020-05-15
=====================
Added
-----
- Version command line option
- Support for Python 3.5
- bump2version support

`0.1.1`_ - 2020-05-14
=====================
Removed
-------
- Unneeded dependency to `funcy`.

`0.1.0`_ - 2020-05-14
=====================
Added
-----
-  pystethoscope tool with the following features:

   Transformers
      -  statement
      -  prereqs
      -  obfuscate
      -  identity
      -  dummy
      -  include-keys
      -  exclude-keys

   Formatters
      -  json
      -  json_pretty
      -  raw

   Predefined pipelines
      -  raw

.. _Unreleased: https://github.com/MonetDBSolutions/monetdb-pystethoscope/compare/v0.4.0...HEAD
.. _0.4.0: https://github.com/MonetDBSolutions/monetdb-pystethoscope/compare/v0.3.2...v0.4.0
.. _0.3.2: https://github.com/MonetDBSolutions/monetdb-pystethoscope/compare/v0.3.1...v0.3.2
.. _0.3.1: https://github.com/MonetDBSolutions/monetdb-pystethoscope/compare/v0.3.0...v0.3.1
.. _0.3.0: https://github.com/MonetDBSolutions/monetdb-pystethoscope/compare/v0.2.0...v0.3.0
.. _0.2.0: https://github.com/MonetDBSolutions/monetdb-pystethoscope/compare/v0.1.3...v0.2.0
.. _0.1.3: https://github.com/MonetDBSolutions/monetdb-pystethoscope/compare/v0.1.2...v0.1.3
.. _0.1.2: https://github.com/MonetDBSolutions/monetdb-pystethoscope/compare/v0.1.1...v0.1.2
.. _0.1.1: https://github.com/MonetDBSolutions/monetdb-pystethoscope/compare/v0.1.0...v0.1.1
.. _0.1.0: https://github.com/MonetDBSolutions/monetdb-pystethoscope/releases/tag/v0.1.0
