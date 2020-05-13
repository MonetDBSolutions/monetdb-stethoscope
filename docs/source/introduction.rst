https://github.com/MonetDBSolutions/monetdb-pystethoscope/workflows/Test%20pystethoscope/badge.svg?branch=master

Introduction
============

``pystethoscope`` is a command line tool to filter and format the events
coming from the MonetDB profiler. This profiler emits two JSON objects,
one at the start and one at the end of every MAL instruction executed.
``pystethoscope`` connects to a MonetDB server process, reads the
objects emitted by the profiler and performs various transformations
specified by the user.

Its name is inspired by the medical device, called a stethoscope. It can
be attached to a body to listen to the lungs and heart. The same holds
for ``pystethoscope``. You can attach it to a running MonetDB server and
immediately see what it is doing.

Conceptually the user specifies a transformation pipeline. The pipeline
is applied to every JSON object emitted by the server and has the
following stages:

Reading
   After a connection to the MonetDB server is established,
   ``pystethoscope`` reads one string, representing a JSON object, from
   the connection.
Parsing
   The string is first parsed into a Python dictionary. The user cannot
   affect the execution of this stage. (But take a look at the ``raw``
   pipeline below).
Transforming
   The various user specified transformers are run on the Python
   dictionary. Transformers add or remove key-value pairs from the
   dictionaries.
Filtering
   Filters remove whole objects from the stream based on a used defined
   predicate. (*not yet implemented*)
Formatting
   Formatters change how the object is displayed to the user.

Installation
============

Installation is done via pip:

.. code:: shell

   pip install monetdb-pystethoscope

This project is compatible with Python >= 3.6.

We recommend the use of virtual environments (see `this
primer <https://realpython.com/python-virtual-environments-a-primer/>`__
if you are unfamiliar) for installing and using
``monetdb-pystethoscope``.

Usage
=====

The general syntax to use ``pystethoscope`` is:

.. code:: shell

   pystethoscope [OPTIONS] DATABASE

The user provides the specification of the desired pipeline using the
following options:

``--transformer`` (``--transformer/-t``)
   ``statement``, ``prereqs``, ``obfuscate``, ``dummy``, and
   ``identity``. Can be specified multiple times.
``--formatter`` (``--formatter/-F``)
   ``json``, ``json_pretty``, and ``line``.

Alternatively the user can specify a number of predefined pipelines
using ``--pipeline`` (``-l``). This option overrides all other given
options.

Connection options
------------------

database
   The name of the database to connect to. This argument is mandatory.
username (``--username/-u username``)
   The name of the user for the database connection. The default value
   is ``monetdb``.
password (``--password/-P password``)
   The password to be used for the database connection. If this option
   is not specified, ``pystethoscope`` will prompt the user for a
   password.

Reading and Parsing
-------------------

Reading and parsing happen automatically in every pipeline, (with the
exception of the ``raw`` pipeline as specified below), and as such the
user does not have any control over it.

Transforming
------------

The user can specify a number of transformers that can change the
content of the JSON objects. Most transformers add key-value pairs in
objects. Currently ``pystethoscope`` implements the following
transformers:

statement
   Recreates a rendering of the MAL statement that this object
   represents. This transformer adds the key ``stmt`` in the JSON object
   with a string value that represents the MAL statement.
prereqs
   Adds the key ``prereq`` in the JSON object. Its value is a list of
   program counter values (see section *MAL profiler JSON format*) of
   MAL instructions that need to be completed before the current
   instruction can start executing.
obfuscate
   This transformer replaces all the literal values in the JSON object
   with three asterisks.
identity
   This transformer leaves the object unchanged. In itself this is not
   particularly useful to the user, but it might be useful in the future
   as a base case for recursive transformers and to denote the absence
   of other operations.
dummy
   This transformer adds the key ``L0`` with a value ``'dummy value'``.
   This is used mostly for debugging.

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
json\ :sub:`pretty`
   Formats the object as a human readable valid JSON string.
line
   Presents the values in the object in one line separated by the string
   ``,\t`` and enclosed in square brackets.
raw
   Sends the object as is to the output stream. This usually uses the
   default Python rendering for dictionaries. The exception to this rule
   is the raw pipeline.

Predefined pipelines
--------------------

The following are the predefined pipelines that ``pystethoscope``
currently has:

raw
   This pipeline is intended for accessing the raw output of the MonetDB
   server's profiler. When using this pipeline ``pystethoscope`` will
   connect to the server read strings and print them to the output
   stream. No other processing happens, and specifically *no parsing
   takes place*. This is mainly useful for debugging the profiler module
   of the MonetDB server.

MAL profiler JSON format
========================

The MAL profiler events are relevant for both end-users to identify
expensive relational operators or intermediate sizes, but it is also
used by the MonetDB development team to expose some internal states. The
JSON objects emitted by the MonetDB profiler may contain the following
fields:

version
   The MonetDB server version. If it is an unreleased version it
   includes the mercurial commit id of the code base used to compile the
   server.
user
   The id of the user running the queries.
clk
   nanoseconds since the UNIX epoch.
mclk
   nanoseconds since the start of the MonetDB server.
thread
   The id of the thread that executes this instruction.
program
   The full name of the MAL block containing this instruction.
pc
   The program counter.
tag
   The identifier of the MAL block containing this instruction.
module
   The name of the MAL module that defines this instruction.
function
   The name of the MAL block containing this instruction.
barrier
   The instruction starts a repetition block.
operator
   The MAL language operator that defines this MAL block.
session
   A UUID that identifies the MonetDB server process.
state
   What is the execution state for this instruction [start,done].
args
   An array containing information about the arguments and return values
   of this instruction.
ret/arg
   The index of the variable in the sequence of return values/arguments.
var
   The variable name.
alias
   The fully qualified name (``schema.table.name``) of the SQL column
   that corresponds to this variable if available.
type
   The variable MAL type.
const
   1 if the variable is a constant, known at query compile time, or 0
   otherwise.
value
   The variable value.
eol
   The end-of-life (end-of-scope) of a variable in a MAL program.

Additionally if the variable's type is BAT, a sequence of basic types,
then a number of extra fields may be shown:

view
   "true" if the BAT is a view (no storage overhead), "false" otherwise.
persistence
   "persistent" or "transient".
sorted
   1 if the values in the bat are sorted in ascending order, 0
   otherwise.
revsorted
   1 if the values it the bat are sorted in descending order, 0
   otherwise.
nonil
   1 if the BAT does **not** contain nil values.
nil
   1 if the BAT contains nil values.
file
   The filename of the file that contains the BAT if it is persistent.
count
   How many values are there in the BAT.
size
   The total size in bytes of the BAT.
usec
   micro second execution time

Finally there are a number of fields that have been used for debugging
the profiler itself or the MonetDB server more generally. These include:

parent
   For views the BAT it depends on.
seqbase
   The value of the first oid in a BAT.
bid
   Index in the BAT buffer pool.
key
   The column contains unique values.
used
   Detect superflous variables in the MAL plans.
fixed
   Freeze the type of a variable.
udf
   User-defined implementation.

These fields might be dropped or changed in future releases of MonetDB
and applications should NOT depend on them.

Note: The combination of the fields ``session``, ``tag``, and ``pc``
identifies uniquely a single MAL instruction. The combination of
``session``, ``tag``, ``pc`` and ``state``, identifies uniquely a single
JSON object.

Examples
========

In the following examples we will be connecting to a database named
``demo``, with user ``monetdb``, and password ``monetdb``:

Create JSON objects containing only the fields ``pc``, ``clk`` and
``state``

.. code:: shell

   pystethoscope -u monetdb -P monetdb --include-keys pc,clk,state demo

Show the executed statements, with timestamps for the start and the end
of the execution.

.. code:: shell

   pystethoscope -u monetdb -P monetdb --transformer statement --formatter line --include-keys stmt,clk,state demo

The same as above but hide the values in the plan

.. code:: shell

   pystethoscope -u monetdb -P monetdb --transformer statement --transformer obfuscate --formatter line --include-keys stmt,clk,state demo

Pretty print the JSON object after adding statements and prerequisites

.. code:: shell

   pystethoscope -u monetdb -P monetdb -t statement -t prereqs -F json_pretty demo

Developer notes
===============

``pystethoscope`` is developed using
`Poetry <https://python-poetry.org/>`__, for dependency management and
packaging.

Installation for development
----------------------------

In order to install ``pystethoscope`` do the following:

.. code:: shell

   pip3 install --user poetry
   PYTHON_BIN_PATH="$(python3 -m site --user-base)/bin"
   export PATH="$PATH:$PYTHON_BIN_PATH"

   git clone git@github.com:MonetDBSolutions/monetdb-pystethoscope.git
   cd monetdb-pystethoscope
   poetry install
   poetry run pystethoscope --help

On 30/04/2020 `pymonetdb
1.3.1 <https://github.com/gijzelaerr/pymonetdb/releases/tag/1.3.1>`__
was released, which includes a feature needed to connect transparently
to the MonetDB server. If you have installed the development version of
``pystethoscope``, before that date you need to update:

.. code:: shell

   cd monetdb-pystethoscope
   git pull
   poetry update
