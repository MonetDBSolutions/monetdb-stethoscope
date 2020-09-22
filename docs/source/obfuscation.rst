Obfuscation
===========

The purpose of data obfuscation is to not show data values or SQL object identifiers
to the outside user. Although relevant mostly for end-user interaction with
a result set, it can also be applied to the events spit out by MonetDB for
post session analysis and system monitoring.

For a good introduction to data obfuscation techniques consider
http://blough.ece.gatech.edu/research/papers/ieeesp04.pdf

Complete data obfuscation is best implemented with simply masking all literals in a query plan a pattern, e.g. ***
This method is supported by the stethoscope using the -t obfuscation option.

The disadvantage of data masking is that too much is shielded for post-analysis of the system behavior.
A better solution is to use one-way functions, which are also the cornerstone for all
encryption techniques. In general, it is a function of the form f(x)= s * y, where 's' is
considered the secret key. Only if you have a pair (x,f(x) it can be broken.
To reduce the impact of this out of bound leakage of the secret key, its value is
a fresh random number chosen at the start of the trace. Using multiple keys, geared
at a class of values further reduce the potential of leakage.

Furthermore, this mapping is only applied to data that originates in the
database or can be derived from the database by applying an expression.
In its simpliest form a data item is processed by a function that respects
the properties of the underlying domain type, but makes it practically impossible
to invert the original value from the message.

The new obfuscation scheme designed here relies on two elements.
1) DDL obfuscation. Which maps all SQL schema objects to a non-informative alternative.
For example, the column reference finances.personal.salary is mapped to a pattern
schema<S>.table<T>.Column<C> where S,T,C are randomized numbers, whose validity
only holds for a single stethoscope run.

2) Query parameter obfuscation.
The arguments to operators that find their origin in the database are
mapped using a one-way function
    f_type(original) = random * original
where random is different for each column/type and holds for a single stethoscope run.
The type specific obfuscation can lead to an overflow, which renders the
relative ordering within a range predicate meaningless.

The code below is considered a default. It should be easy for the user
to replace it with partial masking or alternative obfuscation schemes.

Beware, the stethoscope only sees the data presented in the queries, which
may not even reflect an item in the database. As such, it is more about
obfuscation of the kind of queries posed to the system at stake.

WARNING the output of the obfuscation should not include recognizable 'filename' with
system paths, 'alias' with recognizable schema information, 'sql.bind' should not
show schema information, ... values in selections and likeselect should not be
recognizable.