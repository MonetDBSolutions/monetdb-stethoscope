Examples
========

In the following examples we will be connecting to a database named ``demo``
with user ``monetdb`` and password ``monetdb``. In each case we will be
executing the SQL query ``SELECT * FROM _tables;`` and we will be showing a part
of the output:

Create JSON objects containing only the fields ``pc``, ``clk`` and ``state``

.. sourcecode:: shell

   pystethoscope -u monetdb -P monetdb --include-keys pc,clk,state demo

.. sourcecode::

   {'clk': 1589451196601447, 'pc': 0, 'state': 'start'}
   {'clk': 1589451196601520, 'pc': 1, 'state': 'start'}
   {'clk': 1589451196601581, 'pc': 1, 'state': 'done'}
   {'clk': 1589451196601605, 'pc': 2, 'state': 'start'}
   {'clk': 1589451196601647, 'pc': 2, 'state': 'done'}
   {'clk': 1589451196601682, 'pc': 3, 'state': 'start'}
   {'clk': 1589451196601719, 'pc': 3, 'state': 'done'}
   {'clk': 1589451196601752, 'pc': 4, 'state': 'start'}
   {'clk': 1589451196601787, 'pc': 4, 'state': 'done'}
   {'clk': 1589451196601816, 'pc': 5, 'state': 'start'}
   {'clk': 1589451196601884, 'pc': 5, 'state': 'done'}
   {'clk': 1589451196601914, 'pc': 6, 'state': 'start'}
   {'clk': 1589451196601947, 'pc': 6, 'state': 'done'}
   {'clk': 1589451196601975, 'pc': 7, 'state': 'start'}
   {'clk': 1589451196601988, 'pc': 7, 'state': 'done'}
   {'clk': 1589451196602001, 'pc': 8, 'state': 'start'}
   {'clk': 1589451196602022, 'pc': 8, 'state': 'done'}
   {'clk': 1589451196602042, 'pc': 9, 'state': 'start'}
   {'clk': 1589451196602089, 'pc': 9, 'state': 'done'}
   {'clk': 1589451196602124, 'pc': 10, 'state': 'start'}
   {'clk': 1589451196602149, 'pc': 10, 'state': 'done'}
   {'clk': 1589451196602175, 'pc': 11, 'state': 'start'}
   {'clk': 1589451196602199, 'pc': 11, 'state': 'done'}
   {'clk': 1589451196602224, 'pc': 12, 'state': 'start'}
   {'clk': 1589451196602256, 'pc': 12, 'state': 'done'}
   {'clk': 1589451196602287, 'pc': 13, 'state': 'start'}
   {'clk': 1589451196602344, 'pc': 13, 'state': 'done'}
   {'clk': 1589451196602371, 'pc': 14, 'state': 'start'}
   {'clk': 1589451196602396, 'pc': 14, 'state': 'done'}
   {'clk': 1589451196602423, 'pc': 15, 'state': 'start'}
   {'clk': 1589451196602444, 'pc': 15, 'state': 'done'}
   {'clk': 1589451196602470, 'pc': 16, 'state': 'start'}
   {'clk': 1589451196602500, 'pc': 16, 'state': 'done'}
   {'clk': 1589451196602536, 'pc': 17, 'state': 'start'}
   {'clk': 1589451196602574, 'pc': 17, 'state': 'done'}
   {'clk': 1589451196602600, 'pc': 18, 'state': 'start'}
   {'clk': 1589451196602625, 'pc': 18, 'state': 'done'}
   {'clk': 1589451196602651, 'pc': 19, 'state': 'start'}
   {'clk': 1589451196602672, 'pc': 19, 'state': 'done'}
   {'clk': 1589451196602695, 'pc': 20, 'state': 'start'}
   {'clk': 1589451196602724, 'pc': 20, 'state': 'done'}
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
   {'clk': 1589451196603230, 'pc': 29, 'state': 'start'}
   {'clk': 1589451196603261, 'pc': 29, 'state': 'done'}
   {'clk': 1589451196603289, 'pc': 30, 'state': 'start'}
   {'clk': 1589451196603313, 'pc': 30, 'state': 'done'}
   {'clk': 1589451196603341, 'pc': 31, 'state': 'start'}
   {'clk': 1589451196603362, 'pc': 31, 'state': 'done'}
   {'clk': 1589451196603384, 'pc': 32, 'state': 'start'}
   {'clk': 1589451196603416, 'pc': 32, 'state': 'done'}
   {'clk': 1589451196603445, 'pc': 33, 'state': 'start'}
   {'clk': 1589451196603478, 'pc': 33, 'state': 'done'}
   {'clk': 1589451196603506, 'pc': 34, 'state': 'start'}
   {'clk': 1589451196603530, 'pc': 34, 'state': 'done'}
   {'clk': 1589451196603555, 'pc': 35, 'state': 'start'}
   {'clk': 1589451196603577, 'pc': 35, 'state': 'done'}
   {'clk': 1589451196603602, 'pc': 36, 'state': 'start'}
   {'clk': 1589451196603643, 'pc': 36, 'state': 'done'}
   {'clk': 1589451196603682, 'pc': 37, 'state': 'start'}
   {'clk': 1589451196603719, 'pc': 37, 'state': 'done'}
   {'clk': 1589451196603748, 'pc': 38, 'state': 'start'}
   {'clk': 1589451196603774, 'pc': 38, 'state': 'done'}
   {'clk': 1589451196603803, 'pc': 39, 'state': 'start'}
   {'clk': 1589451196603826, 'pc': 39, 'state': 'done'}
   {'clk': 1589451196603857, 'pc': 40, 'state': 'start'}
   {'clk': 1589451196603890, 'pc': 40, 'state': 'done'}
   {'clk': 1589451196603923, 'pc': 41, 'state': 'start'}
   {'clk': 1589451196604909, 'pc': 41, 'state': 'done'}
   {'clk': 1589451196605377, 'pc': 42, 'state': 'start'}
   {'clk': 1589451196605519, 'pc': 42, 'state': 'done'}
   {'clk': 1589451196605629, 'pc': 0, 'state': 'done'}


Show the executed statements, with timestamps for the start and the end
of the execution.

.. sourcecode:: shell

   pystethoscope -u monetdb -P monetdb --transformer statement --formatter line --include-keys stmt,clk,state demo

.. sourcecode::

   [1589451477965109,	start,	function user.s4_0();]
   [1589451477965167,	start,	querylog.define(X_1=0@0:void,"select * from _tables;":str,"default_pipe":str,55:int);]
   [1589451477965198,	done,	querylog.define(X_1=0@0:void,"select * from _tables;":str,"default_pipe":str,55:int);]
   [1589451477965229,	start,	bat.pack(X_73=[0]:bat[:str],"sys._tables":str,"sys._tables":str,"sys._tables":str,"sys._tables":str,"sys._tables":str,"sys._tables":str,"sys._tables":str,"sys._tables":str);]
   [1589451477965286,	done,	bat.pack(X_73=[8]:bat[:str],"sys._tables":str,"sys._tables":str,"sys._tables":str,"sys._tables":str,"sys._tables":str,"sys._tables":str,"sys._tables":str,"sys._tables":str);]
   [1589451477965331,	start,	bat.pack(X_74=[0]:bat[:str],"id":str,"name":str,"schema_id":str,"query":str,"type":str,"system":str,"commit_action":str,"access":str);]
   [1589451477965381,	done,	bat.pack(X_74=[8]:bat[:str],"id":str,"name":str,"schema_id":str,"query":str,"type":str,"system":str,"commit_action":str,"access":str);]
   [1589451477965425,	start,	bat.pack(X_75=[0]:bat[:str],"int":str,"varchar":str,"int":str,"varchar":str,"smallint":str,"boolean":str,"smallint":str,"smallint":str);]
   [1589451477965471,	done,	bat.pack(X_75=[8]:bat[:str],"int":str,"varchar":str,"int":str,"varchar":str,"smallint":str,"boolean":str,"smallint":str,"smallint":str);]
   [1589451477965509,	start,	bat.pack(X_76=[0]:bat[:int],32:int,1024:int,32:int,1048576:int,16:int,1:int,16:int,16:int);]
   [1589451477965548,	done,	bat.pack(X_76=[8]:bat[:int],32:int,1024:int,32:int,1048576:int,16:int,1:int,16:int,16:int);]
   [1589451477965585,	start,	bat.pack(X_77=[0]:bat[:int],0:int,0:int,0:int,0:int,0:int,0:int,0:int,0:int);]
   [1589451477965622,	done,	bat.pack(X_77=[8]:bat[:int],0:int,0:int,0:int,0:int,0:int,0:int,0:int,0:int);]
   [1589451477965657,	start,	sql.mvc(X_4=0:int);]
   [1589451477965677,	done,	sql.mvc(X_4=0:int);]
   [1589451477965692,	start,	sql.tid(C_5=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str);]
   [1589451477965718,	done,	sql.tid(C_5=[86]:bat[:oid],X_4=0:int,"sys":str,"_tables":str);]
   [1589451477965744,	start,	sql.bind(X_17=[0]:bat[:int],X_4=0:int,"sys":str,"_tables":str,"id":str,0:int);]
   [1589451477965773,	done,	sql.bind(X_17=[86]:bat[:int],X_4=0:int,"sys":str,"_tables":str,"id":str,0:int);]
   [1589451477965818,	start,	X_20:bat[:int] := sql.bind(X_19=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str,"id":str,2:int);]
   [1589451477965869,	done,	X_20:bat[:int] := sql.bind(X_19=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str,"id":str,2:int);]
   [1589451477965924,	start,	sql.bind(X_18=[0]:bat[:int],X_4=0:int,"sys":str,"_tables":str,"id":str,1:int);]
   [1589451477965970,	done,	sql.bind(X_18=[0]:bat[:int],X_4=0:int,"sys":str,"_tables":str,"id":str,1:int);]
   [1589451477966017,	start,	sql.projectdelta(X_64=[0]:bat[:int],C_5=[86]:bat[:oid],X_17=[86]:bat[:int],X_19=[0]:bat[:oid],X_20=[0]:bat[:int],X_18=[0]:bat[:int]);]
   [1589451477966082,	done,	sql.projectdelta(X_64=[86]:bat[:int],C_5=[86]:bat[:oid],X_17=[86]:bat[:int],X_19=[0]:bat[:oid],X_20=[0]:bat[:int],X_18=[0]:bat[:int]);]
   [1589451477966153,	start,	sql.bind(X_22=[0]:bat[:str],X_4=0:int,"sys":str,"_tables":str,"name":str,0:int);]
   [1589451477966200,	done,	sql.bind(X_22=[86]:bat[:str],X_4=0:int,"sys":str,"_tables":str,"name":str,0:int);]
   [1589451477966249,	start,	X_26:bat[:str] := sql.bind(X_25=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str,"name":str,2:int);]
   [1589451477966302,	done,	X_26:bat[:str] := sql.bind(X_25=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str,"name":str,2:int);]
   [1589451477966360,	start,	sql.bind(X_24=[0]:bat[:str],X_4=0:int,"sys":str,"_tables":str,"name":str,1:int);]
   [1589451477966406,	done,	sql.bind(X_24=[0]:bat[:str],X_4=0:int,"sys":str,"_tables":str,"name":str,1:int);]
   [1589451477966454,	start,	sql.projectdelta(X_65=[0]:bat[:str],C_5=[86]:bat[:oid],X_22=[86]:bat[:str],X_25=[0]:bat[:oid],X_26=[0]:bat[:str],X_24=[0]:bat[:str]);]
   [1589451477966517,	done,	sql.projectdelta(X_65=[86]:bat[:str],C_5=[86]:bat[:oid],X_22=[86]:bat[:str],X_25=[0]:bat[:oid],X_26=[0]:bat[:str],X_24=[0]:bat[:str]);]
   [1589451477966585,	start,	sql.bind(X_28=[0]:bat[:int],X_4=0:int,"sys":str,"_tables":str,"schema_id":str,0:int);]
   [1589451477966633,	done,	sql.bind(X_28=[86]:bat[:int],X_4=0:int,"sys":str,"_tables":str,"schema_id":str,0:int);]
   [1589451477966680,	start,	X_32:bat[:int] := sql.bind(X_31=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str,"schema_id":str,2:int);]
   [1589451477966734,	done,	X_32:bat[:int] := sql.bind(X_31=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str,"schema_id":str,2:int);]
   [1589451477966789,	start,	sql.bind(X_30=[0]:bat[:int],X_4=0:int,"sys":str,"_tables":str,"schema_id":str,1:int);]
   [1589451477966834,	done,	sql.bind(X_30=[0]:bat[:int],X_4=0:int,"sys":str,"_tables":str,"schema_id":str,1:int);]
   [1589451477966887,	start,	sql.projectdelta(X_66=[0]:bat[:int],C_5=[86]:bat[:oid],X_28=[86]:bat[:int],X_31=[0]:bat[:oid],X_32=[0]:bat[:int],X_30=[0]:bat[:int]);]
   [1589451477966948,	done,	sql.projectdelta(X_66=[86]:bat[:int],C_5=[86]:bat[:oid],X_28=[86]:bat[:int],X_31=[0]:bat[:oid],X_32=[0]:bat[:int],X_30=[0]:bat[:int]);]
   [1589451477967015,	start,	sql.bind(X_34=[0]:bat[:str],X_4=0:int,"sys":str,"_tables":str,"query":str,0:int);]
   [1589451477967062,	done,	sql.bind(X_34=[86]:bat[:str],X_4=0:int,"sys":str,"_tables":str,"query":str,0:int);]
   [1589451477967115,	start,	X_38:bat[:str] := sql.bind(X_37=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str,"query":str,2:int);]
   [1589451477967165,	done,	X_38:bat[:str] := sql.bind(X_37=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str,"query":str,2:int);]
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
   [1589451477968063,	start,	sql.bind(X_48=[0]:bat[:bit],X_4=0:int,"sys":str,"_tables":str,"system":str,1:int);]
   [1589451477968109,	done,	sql.bind(X_48=[0]:bat[:bit],X_4=0:int,"sys":str,"_tables":str,"system":str,1:int);]
   [1589451477968156,	start,	sql.projectdelta(X_69=[0]:bat[:bit],C_5=[86]:bat[:oid],X_46=[86]:bat[:bit],X_49=[0]:bat[:oid],X_50=[0]:bat[:bit],X_48=[0]:bat[:bit]);]
   [1589451477968216,	done,	sql.projectdelta(X_69=[86]:bat[:bit],C_5=[86]:bat[:oid],X_46=[86]:bat[:bit],X_49=[0]:bat[:oid],X_50=[0]:bat[:bit],X_48=[0]:bat[:bit]);]
   [1589451477968276,	start,	sql.bind(X_52=[0]:bat[:sht],X_4=0:int,"sys":str,"_tables":str,"commit_action":str,0:int);]
   [1589451477968323,	done,	sql.bind(X_52=[86]:bat[:sht],X_4=0:int,"sys":str,"_tables":str,"commit_action":str,0:int);]
   [1589451477968372,	start,	X_56:bat[:sht] := sql.bind(X_55=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str,"commit_action":str,2:int);]
   [1589451477968423,	done,	X_56:bat[:sht] := sql.bind(X_55=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str,"commit_action":str,2:int);]
   [1589451477968477,	start,	sql.bind(X_54=[0]:bat[:sht],X_4=0:int,"sys":str,"_tables":str,"commit_action":str,1:int);]
   [1589451477968542,	done,	sql.bind(X_54=[0]:bat[:sht],X_4=0:int,"sys":str,"_tables":str,"commit_action":str,1:int);]
   [1589451477968584,	start,	sql.projectdelta(X_70=[0]:bat[:sht],C_5=[86]:bat[:oid],X_52=[86]:bat[:sht],X_55=[0]:bat[:oid],X_56=[0]:bat[:sht],X_54=[0]:bat[:sht]);]
   [1589451477968634,	done,	sql.projectdelta(X_70=[86]:bat[:sht],C_5=[86]:bat[:oid],X_52=[86]:bat[:sht],X_55=[0]:bat[:oid],X_56=[0]:bat[:sht],X_54=[0]:bat[:sht]);]
   [1589451477968685,	start,	sql.bind(X_58=[0]:bat[:sht],X_4=0:int,"sys":str,"_tables":str,"access":str,0:int);]
   [1589451477968723,	done,	sql.bind(X_58=[86]:bat[:sht],X_4=0:int,"sys":str,"_tables":str,"access":str,0:int);]
   [1589451477968761,	start,	X_62:bat[:sht] := sql.bind(X_61=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str,"access":str,2:int);]
   [1589451477968802,	done,	X_62:bat[:sht] := sql.bind(X_61=[0]:bat[:oid],X_4=0:int,"sys":str,"_tables":str,"access":str,2:int);]
   [1589451477968850,	start,	sql.bind(X_60=[0]:bat[:sht],X_4=0:int,"sys":str,"_tables":str,"access":str,1:int);]
   [1589451477968886,	done,	sql.bind(X_60=[0]:bat[:sht],X_4=0:int,"sys":str,"_tables":str,"access":str,1:int);]
   [1589451477968927,	start,	sql.projectdelta(X_71=[0]:bat[:sht],C_5=[86]:bat[:oid],X_58=[86]:bat[:sht],X_61=[0]:bat[:oid],X_62=[0]:bat[:sht],X_60=[0]:bat[:sht]);]
   [1589451477968976,	done,	sql.projectdelta(X_71=[86]:bat[:sht],C_5=[86]:bat[:oid],X_58=[86]:bat[:sht],X_61=[0]:bat[:oid],X_62=[0]:bat[:sht],X_60=[0]:bat[:sht]);]
   [1589451477969030,	start,	sql.resultSet(X_72=0:int,X_73=[8]:bat[:str],X_74=[8]:bat[:str],X_75=[8]:bat[:str],X_76=[8]:bat[:int],X_77=[8]:bat[:int],X_64=[86]:bat[:int],X_65=[86]:bat[:str],X_66=[86]:bat[:int],X_67=[86]:bat[:str],X_68=[86]:bat[:sht],X_69=[86]:bat[:bit],X_70=[86]:bat[:sht],X_71=[86]:bat[:sht]);]
   [1589451477970099,	done,	sql.resultSet(X_72=2:int,X_73=[8]:bat[:str],X_74=[8]:bat[:str],X_75=[8]:bat[:str],X_76=[8]:bat[:int],X_77=[8]:bat[:int],X_64=[86]:bat[:int],X_65=[86]:bat[:str],X_66=[86]:bat[:int],X_67=[86]:bat[:str],X_68=[86]:bat[:sht],X_69=[86]:bat[:bit],X_70=[86]:bat[:sht],X_71=[86]:bat[:sht]);]
   [1589451477970285,	start,	end user.s4_0]
   [1589451477970309,	done,	end user.s4_0]
   [1589451477970326,	done,	function user.s4_0();]


The same as above but hide the values in the plan

.. sourcecode:: shell

   pystethoscope -u monetdb -P monetdb --transformer statement --transformer obfuscate --formatter line --include-keys stmt,clk,state demo

.. sourcecode::

   [1589451636932943,	start,	function user.s4_0();]
   [1589451636933017,	start,	querylog.define(X_1=0@0:void,***:str,***:str,***:int);]
   [1589451636933072,	done,	querylog.define(X_1=0@0:void,***:str,***:str,***:int);]
   [1589451636933117,	start,	bat.pack(X_73=[0]:bat[:str],***:str,***:str,***:str,***:str,***:str,***:str,***:str,***:str);]
   [1589451636933199,	done,	bat.pack(X_73=[8]:bat[:str],***:str,***:str,***:str,***:str,***:str,***:str,***:str,***:str);]
   [1589451636933268,	start,	bat.pack(X_74=[0]:bat[:str],***:str,***:str,***:str,***:str,***:str,***:str,***:str,***:str);]
   [1589451636933343,	done,	bat.pack(X_74=[8]:bat[:str],***:str,***:str,***:str,***:str,***:str,***:str,***:str,***:str);]
   [1589451636933410,	start,	bat.pack(X_75=[0]:bat[:str],***:str,***:str,***:str,***:str,***:str,***:str,***:str,***:str);]
   [1589451636933480,	done,	bat.pack(X_75=[8]:bat[:str],***:str,***:str,***:str,***:str,***:str,***:str,***:str,***:str);]
   [1589451636933538,	start,	bat.pack(X_76=[0]:bat[:int],***:int,***:int,***:int,***:int,***:int,***:int,***:int,***:int);]
   [1589451636933597,	done,	bat.pack(X_76=[8]:bat[:int],***:int,***:int,***:int,***:int,***:int,***:int,***:int,***:int);]
   [1589451636933652,	start,	bat.pack(X_77=[0]:bat[:int],***:int,***:int,***:int,***:int,***:int,***:int,***:int,***:int);]
   [1589451636933706,	done,	bat.pack(X_77=[8]:bat[:int],***:int,***:int,***:int,***:int,***:int,***:int,***:int,***:int);]
   [1589451636933761,	start,	sql.mvc(X_4=***:int);]
   [1589451636933784,	done,	sql.mvc(X_4=***:int);]
   [1589451636933806,	start,	sql.tid(C_5=[0]:bat[:oid],X_4=***:int,***:str,***:str);]
   [1589451636933850,	done,	sql.tid(C_5=[86]:bat[:oid],X_4=***:int,***:str,***:str);]
   [1589451636933889,	start,	sql.bind(X_17=[0]:bat[:int],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636933934,	done,	sql.bind(X_17=[86]:bat[:int],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636933978,	start,	X_20:bat[:int] := sql.bind(X_19=[0]:bat[:oid],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636934026,	done,	X_20:bat[:int] := sql.bind(X_19=[0]:bat[:oid],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636934078,	start,	sql.bind(X_18=[0]:bat[:int],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636934121,	done,	sql.bind(X_18=[0]:bat[:int],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636934165,	start,	sql.projectdelta(X_64=[0]:bat[:int],C_5=[86]:bat[:oid],X_17=[86]:bat[:int],X_19=[0]:bat[:oid],X_20=[0]:bat[:int],X_18=[0]:bat[:int]);]
   [1589451636934227,	done,	sql.projectdelta(X_64=[86]:bat[:int],C_5=[86]:bat[:oid],X_17=[86]:bat[:int],X_19=[0]:bat[:oid],X_20=[0]:bat[:int],X_18=[0]:bat[:int]);]
   [1589451636934287,	start,	sql.bind(X_22=[0]:bat[:str],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636934331,	done,	sql.bind(X_22=[86]:bat[:str],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636934376,	start,	X_26:bat[:str] := sql.bind(X_25=[0]:bat[:oid],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636934424,	done,	X_26:bat[:str] := sql.bind(X_25=[0]:bat[:oid],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636934474,	start,	sql.bind(X_24=[0]:bat[:str],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636934519,	done,	sql.bind(X_24=[0]:bat[:str],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636934564,	start,	sql.projectdelta(X_65=[0]:bat[:str],C_5=[86]:bat[:oid],X_22=[86]:bat[:str],X_25=[0]:bat[:oid],X_26=[0]:bat[:str],X_24=[0]:bat[:str]);]
   [1589451636934623,	done,	sql.projectdelta(X_65=[86]:bat[:str],C_5=[86]:bat[:oid],X_22=[86]:bat[:str],X_25=[0]:bat[:oid],X_26=[0]:bat[:str],X_24=[0]:bat[:str]);]
   [1589451636934696,	start,	sql.bind(X_28=[0]:bat[:int],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636934741,	done,	sql.bind(X_28=[86]:bat[:int],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636934786,	start,	X_32:bat[:int] := sql.bind(X_31=[0]:bat[:oid],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636934834,	done,	X_32:bat[:int] := sql.bind(X_31=[0]:bat[:oid],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636934884,	start,	sql.bind(X_30=[0]:bat[:int],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636934928,	done,	sql.bind(X_30=[0]:bat[:int],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636934971,	start,	sql.projectdelta(X_66=[0]:bat[:int],C_5=[86]:bat[:oid],X_28=[86]:bat[:int],X_31=[0]:bat[:oid],X_32=[0]:bat[:int],X_30=[0]:bat[:int]);]
   [1589451636935028,	done,	sql.projectdelta(X_66=[86]:bat[:int],C_5=[86]:bat[:oid],X_28=[86]:bat[:int],X_31=[0]:bat[:oid],X_32=[0]:bat[:int],X_30=[0]:bat[:int]);]
   [1589451636935087,	start,	sql.bind(X_34=[0]:bat[:str],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636935149,	done,	sql.bind(X_34=[86]:bat[:str],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636935209,	start,	X_38:bat[:str] := sql.bind(X_37=[0]:bat[:oid],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636935258,	done,	X_38:bat[:str] := sql.bind(X_37=[0]:bat[:oid],X_4=***:int,***:str,***:str,***:str,***:int);]
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
   [1589451636936100,	start,	sql.bind(X_48=[0]:bat[:bit],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636936149,	done,	sql.bind(X_48=[0]:bat[:bit],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636936195,	start,	sql.projectdelta(X_69=[0]:bat[:bit],C_5=[86]:bat[:oid],X_46=[86]:bat[:bit],X_49=[0]:bat[:oid],X_50=[0]:bat[:bit],X_48=[0]:bat[:bit]);]
   [1589451636936253,	done,	sql.projectdelta(X_69=[86]:bat[:bit],C_5=[86]:bat[:oid],X_46=[86]:bat[:bit],X_49=[0]:bat[:oid],X_50=[0]:bat[:bit],X_48=[0]:bat[:bit]);]
   [1589451636936314,	start,	sql.bind(X_52=[0]:bat[:sht],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636936359,	done,	sql.bind(X_52=[86]:bat[:sht],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636936407,	start,	X_56:bat[:sht] := sql.bind(X_55=[0]:bat[:oid],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636936454,	done,	X_56:bat[:sht] := sql.bind(X_55=[0]:bat[:oid],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636936504,	start,	sql.bind(X_54=[0]:bat[:sht],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636936547,	done,	sql.bind(X_54=[0]:bat[:sht],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636936591,	start,	sql.projectdelta(X_70=[0]:bat[:sht],C_5=[86]:bat[:oid],X_52=[86]:bat[:sht],X_55=[0]:bat[:oid],X_56=[0]:bat[:sht],X_54=[0]:bat[:sht]);]
   [1589451636936648,	done,	sql.projectdelta(X_70=[86]:bat[:sht],C_5=[86]:bat[:oid],X_52=[86]:bat[:sht],X_55=[0]:bat[:oid],X_56=[0]:bat[:sht],X_54=[0]:bat[:sht]);]
   [1589451636936706,	start,	sql.bind(X_58=[0]:bat[:sht],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636936752,	done,	sql.bind(X_58=[86]:bat[:sht],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636936812,	start,	X_62:bat[:sht] := sql.bind(X_61=[0]:bat[:oid],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636936860,	done,	X_62:bat[:sht] := sql.bind(X_61=[0]:bat[:oid],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636936911,	start,	sql.bind(X_60=[0]:bat[:sht],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636936954,	done,	sql.bind(X_60=[0]:bat[:sht],X_4=***:int,***:str,***:str,***:str,***:int);]
   [1589451636936998,	start,	sql.projectdelta(X_71=[0]:bat[:sht],C_5=[86]:bat[:oid],X_58=[86]:bat[:sht],X_61=[0]:bat[:oid],X_62=[0]:bat[:sht],X_60=[0]:bat[:sht]);]
   [1589451636937055,	done,	sql.projectdelta(X_71=[86]:bat[:sht],C_5=[86]:bat[:oid],X_58=[86]:bat[:sht],X_61=[0]:bat[:oid],X_62=[0]:bat[:sht],X_60=[0]:bat[:sht]);]
   [1589451636937116,	start,	sql.resultSet(X_72=***:int,X_73=[8]:bat[:str],X_74=[8]:bat[:str],X_75=[8]:bat[:str],X_76=[8]:bat[:int],X_77=[8]:bat[:int],X_64=[86]:bat[:int],X_65=[86]:bat[:str],X_66=[86]:bat[:int],X_67=[86]:bat[:str],X_68=[86]:bat[:sht],X_69=[86]:bat[:bit],X_70=[86]:bat[:sht],X_71=[86]:bat[:sht]);]
   [1589451636938367,	done,	sql.resultSet(X_72=***:int,X_73=[8]:bat[:str],X_74=[8]:bat[:str],X_75=[8]:bat[:str],X_76=[8]:bat[:int],X_77=[8]:bat[:int],X_64=[86]:bat[:int],X_65=[86]:bat[:str],X_66=[86]:bat[:int],X_67=[86]:bat[:str],X_68=[86]:bat[:sht],X_69=[86]:bat[:bit],X_70=[86]:bat[:sht],X_71=[86]:bat[:sht]);]
   [1589451636938598,	start,	end user.s4_0]
   [1589451636938625,	done,	end user.s4_0]
   [1589451636938644,	done,	function user.s4_0();]


Pretty print the JSON object after adding statements and prerequisites

.. sourcecode:: shell

   pystethoscope -u monetdb -P monetdb -t statement -t prereqs -F json_pretty demo

.. sourcecode::

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
