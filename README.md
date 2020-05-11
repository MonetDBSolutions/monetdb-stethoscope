![Test pystethoscope](https://github.com/MonetDBSolutions/monetdb-profiler-tools/workflows/Test%20pystethoscope/badge.svg)

Introduction
============

`pystethoscope` is a command line tool to filter and format the events
coming from the MonetDB profiler. The MonetDB profiler emits two JSON
objects, one at the start and one at the end of every MAL instruction
executed. `pystethoscope` connects to a MonetDB server process, reads
the objects emitted by the profiler and performs various transformations
specified by the user.

Conceptually the user specifies transformation pipelines. The pipeline
is applied to every JSON object emitted by the server and has the
following stages:

Reading
:   After a connection to the MonetDB server is established,
    `pystethoscope` reads one string, representing a JSON object, from
    the connection.

Parsing
:   The string is first parsed into a Python dictionary. The user cannot
    affect the execution of this stage. (But take a look at the `raw`
    pipeline below).

Transforming
:   The various user specified transformers are run on the Python
    dictionary. Transformers add or remove key-value pairs from the
    dictionaries.

Filtering
:   Filters remove whole objects from the stream based on a used defined
    predicate. (*not yet implemented*)

Formatting
:   Formatters change how the object is displayed to the user.

Usage
=====

The user provides the specification of the desired pipeline using the
command line using the following options:

`--transformer` (`-t`)
:   `statement`, `prereqs`, `obfuscate`, `dummy`, and `identity`. Can be
    specified multiple times.

`--formatter` (`-f`)
:   `json`, `json_pretty`, and `line`.

Alternatively the user can specify a number of predefined pipelines
using `--pipeline` (`-p`). This option overrides all other given
options.

Reading and Parsing
-------------------

Reading and parsing happen automatically in every pipeline, (with the
exception of the `raw` pipeline as specified below), and as such the
user does not have any control over it.

Transforming
------------

The user can specify a number of transformers that can change the
content of the JSON objects. Most transformers add key-value pairs in
objects. Currently `pystethoscope` implements the following
transformers:

statement (`-t statement`)
:   Recreates a rendering of the MAL statement that this object
    represents. This transformer adds the key `stmt` in the JSON object
    with a string value that represents the MAL statement.

prereqs (`-t prereqs`)
:   Adds the key `prereq` in the JSON object. Its value is a list of
    program counter values (see section *MAL profiler JSON format*) of
    MAL instructions that need to be completed before the current
    instruction can start executing.

obfuscate (`-t obfuscate`)
:   This transformer replaces all the literal values in the JSON object
    with three asterisks.

identity (`-t identity`)
:   This transformer leaves the object unchanged. In itself this is not
    particularly useful to the user, but it might be useful in the
    future as a base case for recursive transformers and to denote the
    absence of other operations.

dummy (`-t dummy`)
:   This transformer adds the key `L0` with a value `'dummy
     value'`. This is used mostly for debugging.

### Key inclusion and exclusion transformers

There are two special transformers that take a list of keys as
arguments.

`--include-keys` (`-i key1,key2,...`)
:   This transformer takes a comma separated list of keys and removes
    all other keys from the JSON object.

`--exclude-keys` (`-e key1,key2,...`)
:   This transformer takes a comma separated list of keys and removes
    them from the JSON object.

Formatting
----------

The following formatters are currently available:

json (`-F json`)
:   Formats the object as a valid JSON string.

json~pretty~ (`-F json_pretty`)
:   Formats the object as a human readable valid JSON string.

line (`-F line`)
:   Presents the values in the object in one line separated by the
    string `,\t` and enclosed in square brackets.

raw (`-F raw`)
:   Sends the object as is to the output stream. This usually uses the
    default Python rendering for dictionaries. The exception to this
    rule is the raw pipeline.

Predefined pipelines
--------------------

The following are the predefined pipelines that `pystethoscope`
currently has:

raw (`-p raw`)
:   This pipeline is intended for accessing the raw output of the
    MonetDB server\'s profiler. When using this pipeline `pystethoscope`
    will connect to the server read strings and print them to the output
    stream. No other processing happens, and specifically *no parsing
    takes place*. This is mainly useful for debugging the profiler
    module of the MonetDB server.

Other arguments
---------------

database
:   The name of the database to connect to.

username (`--username/-u username`)
:   The name of the user for the database connection. The default value
    is `monetdb`.

password (`--password/-P password`)
:   The password to be used for the database connection. If this option
    is not specified, `pystethoscope` will prompt its user for a
    password.

MAL profiler JSON format
========================

The JSON objects emitted by the MonetDB profiler may contain the
following fields:

version
:   The MonetDB server version. If it is an unreleased version it
    includes the commit id.

user
:   The id of the user running the queries

clk
:   nanoseconds since the UNIX epoch

mclk
:   nanoseconds since the start of the MonetDB server

thread
:   The id of the thread that executes this instruction

program
:   The full name of the MAL block containing this instruction

pc
:   The program counter

tag
:   The identifier of the MAL block containing this instruction

module
:   The name of the MAL module that defines this instruction

function
:   The name of the MAL block containing this instruction

operator
:   The MAL language operator that defines this MAL block

session
:   A UUID that identifies the MonetDB server process

state
:   What is the execution state for this instruction

args
:   An array containing information about the variables used as
    arguments and return values of this instruction

ret/arg
:   The index of the variable in the sequence of return values/arguments

var
:   The name of the variable

type
:   The type of the variable

const
:   1 if the variable is a constant, known at query compile time, or 0
    otherwise

value
:   The value of the variable

eol
:   The end-of-life (end-of-scope) of a variable in a MAL program

used
:   Internal marker to identify if the variable is used elsewhere.

fixed
:   The argument type is frozen, i.e. not an :any type.

udf
:   The argument is a User-Defined-Function.

Additionally if the variable\'s type is BAT, then a number of extra
fields may be shown:

view
:   \"true\" if the BAT is a view, \"false\" otherwise

parent

:   

seqbase

:   

persistence
:   \"persistent\" or \"transient\"

sorted
:   1 if the values in the bat are sorted in ascending order, 0
    otherwise

revsorted
:   1 if the values it the bat are sorted in descending order, 0
    otherwise

nonil
:   1 if the BAT does **not** contain nil values

nil
:   1 if the BAT contains nil values

bid

:   

key

:   

file
:   The filename of the file that contains the BAT if it is persistent

count
:   How many values are there in the BAT

Note: The combination of the fields `session`, `tag`, and `pc`
identifies uniquely a single MAL instruction. The combination of
`session`, `tag`, `pc` and `state`, identifies uniquely a single JSON
object

Examples
========

In the following examples we will be connecting to a database named
`demo`, with user `monetdb`, and password `monetdb`:

Create JSON objects containing only the fields `pc`, `clk` and `state`

``` {.shell}
pystethoscope -u monetdb -P monetdb --include-keys pc,clk,state demo
```

Show the executed statements, with timestamps for the start and the end
of the execution.

``` {.shell}
pystethoscope -u monetdb -P monetdb --transformer statement --formatter line --include-keys stmt,clk,state demo
```

The same as above but hide the values in the plan

``` {.shell}
pystethoscope -u monetdb -P monetdb --transformer statement --transformer obfuscate --formatter line --include-keys stmt,clk,state demo
```

Pretty print the JSON object after adding statements and prerequisites

Developer notes
===============

`pystethoscope` is developed using [Poetry](https://python-poetry.org/),
for dependency management and packaging.

Installation for development
----------------------------

In order to install `pystethoscope` do the following:

``` {.shell}
pip3 install --user poetry
git clone git@github.com:MonetDBSolutions/monetdb-profiler-tools.git
cd monetdb-profiler-tools
poetry install
poetry run pystethoscope --help
```

On 30/04/2020 [pymonetdb
1.3.1](https://github.com/gijzelaerr/pymonetdb/releases/tag/1.3.1) was
released, which includes a feature needed to connect transparently to
the MonetDB server. If you have installed the development version of
`pystethoscope`, before that date you need to update:

``` {.shell}
cd monetdb-profiler-tools
git pull
poetry update
```
