.. _section-mal-reference:

MAL profiler JSON format
========================

The MAL profiler events are relevant for both end-users to identify expensive
relational operators or intermediate sizes, and the MonetDB development team to
expose some internal states. The JSON objects emitted by the MonetDB profiler
may contain the following fields:

version
   The MonetDB server version. If it is an unreleased version it
   includes the mercurial commit id of the code base used to compile the
   server.
user
   The id of the SQL user running the queries.
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
   What is the execution state for this instruction. Possible states are "start"
   and "done".
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
   The MAL type of the variable.
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
   1 if the values it the bat are sorted in descending order, 0 otherwise. Note
   that a BAT might be both sorted and revsorted if all its values are equal.
nonil
   1 if the BAT does **not** contain nil values.
nil
   1 if the BAT contains nil values.
key
   1 if the BAT contains unique values.
file
   The filename of the file that contains the BAT if it is persistent.
count
   How many values are there in the BAT.
size
   The total size in bytes of the BAT.
usec
   micro second execution time

Finally there are a number of fields that have been used for debugging the
profiler itself or the MonetDB server more generally. These include:

parent
   For views the BAT it depends on.
seqbase
   The value of the first oid in a BAT.
bid
   Index in the BBP (BAT buffer pool).
used
   Detect superflous variables in the MAL plans.
fixed
   Freeze the type of a variable.
udf
   User-defined implementation.

These fields might be dropped or changed in future releases of MonetDB and
applications should NOT depend on them.

Note: The combination of the fields ``session``, ``tag``, and ``pc`` uniquely
identifies a single MAL instruction. The combination of ``session``, ``tag``,
``pc`` and ``state``, uniquely identifies a single JSON object.
