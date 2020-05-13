Examples
========

In the following examples we will be connecting to a database named ``demo``
with user ``monetdb`` and password ``monetdb``. In each case we will be
executing the SQL query ``SELECT * FROM _tables;`` and we will be showing a part
of the output:

Create JSON objects containing only the fields ``pc``, ``clk`` and ``state``

.. sourcecode:: shell

   pystethoscope -u monetdb -P monetdb --include-keys pc,clk,state demo

Show the executed statements, with timestamps for the start and the end
of the execution.

.. sourcecode:: shell

   pystethoscope -u monetdb -P monetdb --transformer statement --formatter line --include-keys stmt,clk,state demo

The same as above but hide the values in the plan

.. sourcecode:: shell

   pystethoscope -u monetdb -P monetdb --transformer statement --transformer obfuscate --formatter line --include-keys stmt,clk,state demo

Pretty print the JSON object after adding statements and prerequisites

.. sourcecode:: shell

   pystethoscope -u monetdb -P monetdb -t statement -t prereqs -F json_pretty demo
