Examples
========

In the following examples we will be connecting to a database named ``demo``
with user ``monetdb`` and password ``monetdb``. In each case we will be
executing the SQL query ``SELECT * FROM _tables;`` and we will be showing a part
of the output:

Create JSON objects containing only the fields ``pc``, ``clk`` and ``state``

.. sourcecode:: shell

   pystethoscope -u monetdb -P monetdb -d demo --include-keys pc clk state 

::

   ...
   {'clk': 1589451196602757, 'pc': 21, 'state': 'start'}
   {'clk': 1589451196602810, 'pc': 21, 'state': 'done'}
   {'clk': 1589451196602836, 'pc': 22, 'state': 'start'}
   {'clk': 1589451196602860, 'pc': 22, 'state': 'done'}
   {'clk': 1589451196602886, 'pc': 23, 'state': 'start'}
   {'clk': 1589451196602907, 'pc': 23, 'state': 'done'}
   {'clk': 1589451196602929, 'pc': 24, 'state': 'start'}
   {'clk': 1589451196602962, 'pc': 24, 'state': 'done'}
   {'clk': 1589451196602995, 'pc': 25, 'state': 'start'}
   {'clk': 1589451196603033, 'pc': 25, 'state': 'done'}
   {'clk': 1589451196603059, 'pc': 26, 'state': 'start'}
   {'clk': 1589451196603083, 'pc': 26, 'state': 'done'}
   {'clk': 1589451196603118, 'pc': 27, 'state': 'start'}
   {'clk': 1589451196603149, 'pc': 27, 'state': 'done'}
   {'clk': 1589451196603171, 'pc': 28, 'state': 'start'}
   {'clk': 1589451196603201, 'pc': 28, 'state': 'done'}
   ...


Show the executed statements, with timestamps for the start and the end
of the execution.

.. sourcecode:: shell

   pystethoscope -u monetdb -P monetdb -d demo --transformer statement --formatter line --include-keys stmt clk state

::

   ...
   [1589451477967224,	start,	sql.bind(X_36=[0]:bat[:str],X_4=0:int,"sys":str,"_tables":str,"query":str,1:int);]
   [1589451477967269,	done,	sql.bind(X_36=[0]:bat[:str],X_4=0:int,"sys":str,"_tables":str,"query":str,1:int);]
   [1589451477967316,	start,	sql.projectdelta(X_67=[0]:bat[:str],C_5=[86]:bat[:oid],X_34=[86]:bat[:str],X_37=[0]:bat[:oid],X_38=[0]:bat[:str],X_36=[0]:bat[:str]);]
   [1589451477967382,	done,	sql.projectdelta(X_67=[86]:bat[:str],C_5=[86]:bat[:oid],X_34=[86]:bat[:str],X_37=[0]:bat[:oid],X_38=[0]:bat[:str],X_36=[0]:bat[:str]);]
   [1589451477967445,	start,	sql.bind(X_40=[0]:bat[:sht],X_4=0:int,"sys":str,"_tables":str,"type":str,0:int);]
   [1589451477967496,	done,	sql.bind(X_40=[86]:bat[:sht],X_4=0:int,"sys":str,"_tables":str,"type":str,0:int);]
   [1589451477967543,	start,	X_44:bat[:sht] := sql.bind(X_43=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str,"type":str,2:int);]
   [1589451477967594,	done,	X_44:bat[:sht] := sql.bind(X_43=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str,"type":str,2:int);]
   [1589451477967647,	start,	sql.bind(X_42=[0]:bat[:sht],X_4=0:int,"sys":str,"_tables":str,"type":str,1:int);]
   [1589451477967692,	done,	sql.bind(X_42=[0]:bat[:sht],X_4=0:int,"sys":str,"_tables":str,"type":str,1:int);]
   [1589451477967738,	start,	sql.projectdelta(X_68=[0]:bat[:sht],C_5=[86]:bat[:oid],X_40=[86]:bat[:sht],X_43=[0]:bat[:oid],X_44=[0]:bat[:sht],X_42=[0]:bat[:sht]);]
   [1589451477967798,	done,	sql.projectdelta(X_68=[86]:bat[:sht],C_5=[86]:bat[:oid],X_40=[86]:bat[:sht],X_43=[0]:bat[:oid],X_44=[0]:bat[:sht],X_42=[0]:bat[:sht]);]
   [1589451477967860,	start,	sql.bind(X_46=[0]:bat[:bit],X_4=0:int,"sys":str,"_tables":str,"system":str,0:int);]
   [1589451477967907,	done,	sql.bind(X_46=[86]:bat[:bit],X_4=0:int,"sys":str,"_tables":str,"system":str,0:int);]
   [1589451477967954,	start,	X_50:bat[:bit] := sql.bind(X_49=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str,"system":str,2:int);]
   [1589451477968005,	done,	X_50:bat[:bit] := sql.bind(X_49=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str,"system":str,2:int);]
   ...

The same as above but hide the values in the plan

.. sourcecode:: shell

   pystethoscope -u monetdb -P monetdb -d demo --transformer statement mask --formatter line --include-keys stmt clk state

::

   ...
   [1589451636935309,	start,	sql.bind(X_36=[0]:bat[:str],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636935352,	done,	sql.bind(X_36=[0]:bat[:str],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636935397,	start,	sql.projectdelta(X_67=[0]:bat[:str],C_5=[86]:bat[:oid],X_34=[86]:bat[:str],X_37=[0]:bat[:oid],X_38=[0]:bat[:str],X_36=[0]:bat[:str]);]
   [1589451636935455,	done,	sql.projectdelta(X_67=[86]:bat[:str],C_5=[86]:bat[:oid],X_34=[86]:bat[:str],X_37=[0]:bat[:oid],X_38=[0]:bat[:str],X_36=[0]:bat[:str]);]
   [1589451636935515,	start,	sql.bind(X_40=[0]:bat[:sht],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636935558,	done,	sql.bind(X_40=[86]:bat[:sht],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636935606,	start,	X_44:bat[:sht] := sql.bind(X_43=[0]:bat[:oid],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636935654,	done,	X_44:bat[:sht] := sql.bind(X_43=[0]:bat[:oid],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636935705,	start,	sql.bind(X_42=[0]:bat[:sht],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636935748,	done,	sql.bind(X_42=[0]:bat[:sht],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636935792,	start,	sql.projectdelta(X_68=[0]:bat[:sht],C_5=[86]:bat[:oid],X_40=[86]:bat[:sht],X_43=[0]:bat[:oid],X_44=[0]:bat[:sht],X_42=[0]:bat[:sht]);]
   [1589451636935849,	done,	sql.projectdelta(X_68=[86]:bat[:sht],C_5=[86]:bat[:oid],X_40=[86]:bat[:sht],X_43=[0]:bat[:oid],X_44=[0]:bat[:sht],X_42=[0]:bat[:sht]);]
   [1589451636935907,	start,	sql.bind(X_46=[0]:bat[:bit],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636935958,	done,	sql.bind(X_46=[86]:bat[:bit],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636936003,	start,	X_50:bat[:bit] := sql.bind(X_49=[0]:bat[:oid],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636936050,	done,	X_50:bat[:bit] := sql.bind(X_49=[0]:bat[:oid],X_4=***:int,***:str,***:str,***:str,***:int);]
   ...

Pretty print the JSON object after adding statements and prerequisites

.. sourcecode:: shell

   pystethoscope -u monetdb -P monetdb -d demo -t statement -t prereqs -F json_pretty

::

   ...
   {
     "version": "11.37.2 (hg id: 9176fe5083 (git)+)",
     "user": 0,
     "clk": 1589451740987458,
     "mclk": 1097757152,
     "thread": 4,
     "program": "user.s4_0",
     "pc": 2,
     "tag": 786,
     "module": "bat",
     "function": "pack",
     "session": "312ec8eb-38be-4f9b-a2c5-88922fccbea9",
     "state": "done",
     "usec": 153,
     "args": [
       {
         "ret": 0,
         "var": "X_73",
         "type": "bat[:str]",
         "persistence": "transient",
         "sorted": 1,
         "revsorted": 1,
         "nonil": 1,
         "nil": 0,
         "key": 0,
         "file": "tmp_427",
         "bid": 279,
         "count": 8,
         "size": 8220,
         "eol": 41,
         "used": 1,
         "fixed": 1,
         "udf": 0
       },
       {
         "arg": 1,
         "var": "X_78",
         "type": "str",
         "const": 1,
         "value": "\"sys._tables\"",
         "eol": 2,
         "used": 1,
         "fixed": 1,
         "udf": 0
       },
       {
         "arg": 2,
         "var": "X_78",
         "type": "str",
         "const": 1,
         "value": "\"sys._tables\"",
         "eol": 2,
         "used": 1,
         "fixed": 1,
         "udf": 0
       },
       {
         "arg": 3,
         "var": "X_78",
         "type": "str",
         "const": 1,
         "value": "\"sys._tables\"",
         "eol": 2,
         "used": 1,
         "fixed": 1,
         "udf": 0
       },
       {
         "arg": 4,
         "var": "X_78",
         "type": "str",
         "const": 1,
         "value": "\"sys._tables\"",
         "eol": 2,
         "used": 1,
         "fixed": 1,
         "udf": 0
       },
       {
         "arg": 5,
         "var": "X_78",
         "type": "str",
         "const": 1,
         "value": "\"sys._tables\"",
         "eol": 2,
         "used": 1,
         "fixed": 1,
         "udf": 0
       },
       {
         "arg": 6,
         "var": "X_78",
         "type": "str",
         "const": 1,
         "value": "\"sys._tables\"",
         "eol": 2,
         "used": 1,
         "fixed": 1,
         "udf": 0
       },
       {
         "arg": 7,
         "var": "X_78",
         "type": "str",
         "const": 1,
         "value": "\"sys._tables\"",
         "eol": 2,
         "used": 1,
         "fixed": 1,
         "udf": 0
       },
       {
         "arg": 8,
         "var": "X_78",
         "type": "str",
         "const": 1,
         "value": "\"sys._tables\"",
         "eol": 2,
         "used": 1,
         "fixed": 1,
         "udf": 0
       }
     ],
     "stmt": "bat.pack(X_73=[8]:bat[:str],\"sys._tables\":str,\"sys._tables\":str,\"sys._tables\":str,\"sys._tables\":str,\"sys._tables\":str,\"sys._tables\":str,\"sys._tables\":str,\"sys._tables\":str);",
     "prereq": [
       2
     ]
   }
   {
     "version": "11.37.2 (hg id: 9176fe5083 (git)+)",
     "user": 0,
     "clk": 1589451740987607,
     "mclk": 1097757301,
     "thread": 4,
     "program": "user.s4_0",
     "pc": 3,
     "tag": 786,
     "module": "bat",
     "function": "pack",
     "session": "312ec8eb-38be-4f9b-a2c5-88922fccbea9",
     "state": "start",
     "usec": 0,
     "args": [
       {
         "ret": 0,
         "var": "X_74",
         "type": "bat[:str]",
         "bid": 0,
         "count": 0,
         "size": 0,
         "eol": 41,
         "used": 1,
         "fixed": 1,
         "udf": 0
       },
       {
         "arg": 1,
         "var": "X_9",
         "type": "str",
         "const": 1,
         "value": "\"id\"",
         "eol": 11,
         "used": 1,
         "fixed": 1,
         "udf": 0
       },
       {
         "arg": 2,
         "var": "X_23",
         "type": "str",
         "const": 1,
         "value": "\"name\"",
         "eol": 15,
         "used": 1,
         "fixed": 1,
         "udf": 0
       },
       {
         "arg": 3,
         "var": "X_29",
         "type": "str",
         "const": 1,
         "value": "\"schema_id\"",
         "eol": 19,
         "used": 1,
         "fixed": 1,
         "udf": 0
       },
       {
         "arg": 4,
         "var": "X_35",
         "type": "str",
         "const": 1,
         "value": "\"query\"",
         "eol": 23,
         "used": 1,
         "fixed": 1,
         "udf": 0
       },
       {
         "arg": 5,
         "var": "X_41",
         "type": "str",
         "const": 1,
         "value": "\"type\"",
         "eol": 27,
         "used": 1,
         "fixed": 1,
         "udf": 0
       },
       {
         "arg": 6,
         "var": "X_47",
         "type": "str",
         "const": 1,
         "value": "\"system\"",
         "eol": 31,
         "used": 1,
         "fixed": 1,
         "udf": 0
       },
       {
         "arg": 7,
         "var": "X_53",
         "type": "str",
         "const": 1,
         "value": "\"commit_action\"",
         "eol": 35,
         "used": 1,
         "fixed": 1,
         "udf": 0
       },
       {
         "arg": 8,
         "var": "X_59",
         "type": "str",
         "const": 1,
         "value": "\"access\"",
         "eol": 39,
         "used": 1,
         "fixed": 1,
         "udf": 0
       }
     ],
     "stmt": "bat.pack(X_74=[0]:bat[:str],\"id\":str,\"name\":str,\"schema_id\":str,\"query\":str,\"type\":str,\"system\":str,\"commit_action\":str,\"access\":str);",
     "prereq": [
       3
     ]
   }
   ...
