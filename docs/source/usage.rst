Usage
=====

The general syntax to use ``stethoscope`` is:

.. code:: shell

   stethoscope [OPTIONS] -d DATABASE

or

.. code:: shell

   stethoscope [OPTIONS] -I FILE

The user provides the specification of the desired pipeline using the
following options:

``--transformer`` (``--transformer/-t``)
   ``statement``, ``prereqs``, ``obfuscate``, ``mask``, ``dummy``, and
   ``identity``. Can be specified in any order multiple times.
``--formatter`` (``--formatter/-F``)
   ``json``, ``json_pretty``, ``line``, and ``raw``.

Alternatively the user can specify a number of predefined pipelines using
``--pipeline`` (``-l``) (see section :ref:`section-predefined-pipelines`). This
option overrides all other given options.

Connection and filesystem options
---------------------------------

database (``--database/-d database``)
   The name of the database to connect to. Either this or the ``--input`` must
   be given.

file input (``--input/-I file name``)
   A file from which to get input. Either this or the ``--database`` must be
   given.

username (``--username/-u username``)
   The name of the user for the database connection. The default value
   is ``monetdb``.

password (``--password/-P password``)
   The password to be used for the database connection. The default value
   is ``monetdb``.

output (``--output/-o filename``)
   The file where ``stethoscope`` will write its output. If this is omitted,
   the output will be written to the standard output.

flush (``--flush/-U``)
   Immediatelly flush the output stream.

Logging and reporting options
-----------------------------

During the processing of JSON objects errors and warnings might be
reported. Normally these are handled and emitted separately for each
object, but in order to reduce noise, stethoscope by default will
dispaly the message just the first time it is emitted.

The default configuration outputs events through the python logging
framework. By default it uses the the console logger. The following
options contol the behavior of logging.

``--verbose/-V``
    Show all error and warnings.

``--no-console/-C``
    Disable logging to the console.

``--log-file/-O filename``
    Write log events to ``filename``. Logging in a file logs all the
    events.



Reading and Parsing
-------------------

Reading and parsing happen automatically in every pipeline, (with the exception
of the ``raw`` pipeline as in :ref:`section-predefined-pipelines`), and as such
the user does not have any control over it.

Transforming
------------

The user can specify a number of transformers that can change the
content of the JSON objects. Most transformers add key-value pairs in
objects. Currently ``stethoscope`` implements the following
transformers:

statement
   Recreates a rendering of the MAL statement that this object represents. This
   transformer adds the key ``stmt`` in the JSON object with a string value that
   represents the MAL statement.

   .. warning::

      This transformer will not work with MonetDB server versions
      earlier than Jun2020 (11.37.7).

   .. note::

      Specifying this transformer implicitly adds the key ``stmt`` to
      the list of included keys.

prereqs
   Adds the key ``prereq`` in the JSON object. Its value is a list of program
   counter values (see section :ref:`section-mal-reference`) of MAL instructions
   that need to be completed before the current instruction can start executing.

   .. note::

      Specifying this transformer implicitly adds the key ``prereq``
      to the list of included keys.


mask
   This transformer replaces all the literal values in the JSON object with
   three asterisks.

   .. warning::

      This transformer will not work with MonetDB server versions
      earlier than Jun2020 (11.37.7).

obfuscate
   .. warning::

      This transformer is deprecated and will not work with MonetDB
      server versions Sep2022 (11.45.7) and LATER. At stethoscope
      version 0.5.0 and later it falls back to the mask transformer.

    This transformer uses one-way functions to replace numeric values,
    alphabet reshuffings for strings, and replaces DDL objects with
    dummy names.

identity
   This transformer leaves the object unchanged. In itself this is not
   particularly useful to the user, but it might be useful in the future as a
   base case for recursive transformers and to denote the absence of other
   operations.

dummy
   This transformer adds the key ``L0`` with a value ``'dummy value'``. This is
   used mostly for debugging.

Key inclusion and exclusion transformers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are two special transformers that take a list of keys as
arguments:

``--include-keys`` (``-i key1 key2 ...``)
   This transformer takes a space separated list of keys and removes all
   other keys from the JSON object.
``--exclude-keys`` (``-e key1 key2 ...``)
   This transformer takes a space separated list of keys and removes
   them from the JSON object.

Formatting
----------

The following formatters are currently available:

json
   Formats the object as a valid JSON string.
json_pretty
   Formats the object as a human readable valid JSON string.
line
   Presents the values in the object in one line separated by the string
   ``,\t`` and enclosed in square brackets.
raw
   Sends the object as is to the output stream. This usually uses the
   default Python rendering for dictionaries. The exception to this rule
   is the raw *pipeline* (see :ref:`section-predefined-pipelines`).

.. _section-predefined-pipelines:

Predefined pipelines
--------------------

The following are the predefined pipelines that ``stethoscope``
currently has:

raw
   This pipeline is intended for accessing the raw output of the MonetDB
   server's profiler. When using this pipeline ``stethoscope`` will
   connect to the server, read strings, and print them to the output
   stream. No other processing happens, and specifically *no parsing
   takes place*. This is mainly useful for debugging the profiler module
   of the MonetDB server.

   .. note::

      The ``raw`` pipeline can be used with earlier than Jun2020 versions of MonetDB.
