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
   The various user-specified transformers are run on the Python
   dictionary. Transformers add or remove key-value pairs from the
   dictionaries.
Filtering
   Filters remove whole objects from the stream based on a user defined
   predicate. (*not yet implemented*)
Formatting
   Formatters change how the object is displayed to the user.
