Usage
=====

The general syntax to use ``pystethoscope`` is:

.. code:: shell

   pystethoscope [OPTIONS] DATABASE

The user provides the specification of the desired pipeline using the
following options:

``--transformer`` (``--transformer/-t``)
   ``statement``, ``prereqs``, ``obfuscate``, ``dummy``, and
   ``identity``. Can be specified in any order multiple times.
``--formatter`` (``--formatter/-F``)
   ``json``, ``json_pretty``, and ``line``.

Alternatively the user can specify a number of predefined pipelines using
``--pipeline`` (``-l``) (see section :ref:`section-predefined-pipelines`). This
option overrides all other given options.

Connection and filesystem options
---------------------------------

database
   The name of the database to connect to. This argument is mandatory.
username (``--username/-u username``)
   The name of the user for the database connection. The default value
   is ``monetdb``.
password (``--password/-P password``)
   The password to be used for the database connection. If this option
   is not specified, ``pystethoscope`` will prompt the user for a
   password.
output (``--output/-o filename``)
   The file where ``pystethoscope`` will write its output. If this is omitted,
   the output will be written to the standard output.

Reading and Parsing
-------------------

Reading and parsing happen automatically in every pipeline, (with the exception
of the ``raw`` pipeline as in :ref:`section-predefined-pipelines`), and as such
the user does not have any control over it.

Transforming
------------

The user can specify a number of transformers that can change the
content of the JSON objects. Most transformers add key-value pairs in
objects. Currently ``pystethoscope`` implements the following
transformers:

statement
   Recreates a rendering of the MAL statement that this object represents. This
   transformer adds the key ``stmt`` in the JSON object with a string value that
   represents the MAL statement.

prereqs
   Adds the key ``prereq`` in the JSON object. Its value is a list of program
   counter values (see section :ref:`section-mal-reference`) of MAL instructions
   that need to be completed before the current instruction can start executing.

obfuscate
   This transformer replaces all the literal values in the JSON object with
   three asterisks.

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

``--include-keys`` (``-i key1,key2,...``)
   This transformer takes a comma separated list of keys and removes all
   other keys from the JSON object.
``--exclude-keys`` (``-e key1,key2,...``)
   This transformer takes a comma separated list of keys and removes
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
   is the raw pipeline.

.. _section-predefined-pipelines:

Predefined pipelines
--------------------

The following are the predefined pipelines that ``pystethoscope``
currently has:

raw
   This pipeline is intended for accessing the raw output of the MonetDB
   server's profiler. When using this pipeline ``pystethoscope`` will
   connect to the server, read strings, and print them to the output
   stream. No other processing happens, and specifically *no parsing
   takes place*. This is mainly useful for debugging the profiler module
   of the MonetDB server.
