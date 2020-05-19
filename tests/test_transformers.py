# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.

from json import loads
from monetdb_pystethoscope import transformers


def test_stmt_constructor():
    objs = [
        '{"version":"11.37.2 (hg id: 402f401ed9f8)","user":0,"clk":1589897072240942,"mclk":7293970476,"thread":3,"program":"user.s4_0","pc":9,"tag":38,"module":"algebra","function":"crossproduct","session":"faf1e78f-d8dd-4af6-bcb7-8b94b30edcc7","state":"start","usec":0,"args":[{"ret":0,"var":"X_19","type":"bat[:oid]","bid":0,"count":0,"size":0,"eol":10,"used":1,"fixed":1,"udf":0},{"ret":1,"var":"X_20","type":"bat[:oid]","bid":0,"count":0,"size":0,"eol":11,"used":1,"fixed":1,"udf":0},{"arg":2,"var":"X_13","type":"bat[:hge]","persistence":"transient","sorted":1,"revsorted":0,"nonil":1,"nil":0,"key":1,"file":"tmp_1224","bid":660,"count":99,"size":1584,"eol":12,"used":1,"fixed":1,"udf":1},{"arg":3,"var":"X_13","type":"bat[:hge]","persistence":"transient","sorted":1,"revsorted":0,"nonil":1,"nil":0,"key":1,"file":"tmp_1224","bid":660,"count":99,"size":1584,"eol":12,"used":1,"fixed":1,"udf":1},{"arg":4,"var":"X_21","type":"bit","const":1,"value":"false","eol":9,"used":1,"fixed":1,"udf":0}]}',
        '{"version":"11.37.2 (hg id: 402f401ed9f8)","user":0,"clk":1589897072241287,"mclk":7293970821,"thread":3,"program":"user.s4_0","pc":10,"tag":38,"module":"generator","function":"projection","session":"faf1e78f-d8dd-4af6-bcb7-8b94b30edcc7","state":"start","usec":0,"args":[{"ret":0,"var":"X_22","type":"bat[:hge]","bid":0,"count":0,"size":0,"eol":14,"used":1,"fixed":1,"udf":0},{"arg":1,"var":"X_19","type":"bat[:oid]","persistence":"transient","sorted":1,"revsorted":0,"nonil":1,"nil":0,"key":0,"file":"tmp_331","bid":217,"count":9801,"size":78408,"eol":10,"used":1,"fixed":1,"udf":0},{"arg":2,"var":"X_13","type":"bat[:hge]","persistence":"transient","sorted":1,"revsorted":0,"nonil":1,"nil":0,"key":1,"file":"tmp_1224","bid":660,"count":99,"size":1584,"eol":12,"used":1,"fixed":1,"udf":1}]}',
    ]
    stmts = [
        'X_20:bat[:oid] := algebra.crossproduct(X_19=[0]:bat[:oid],X_13=[99]:bat[:hge],X_13=[99]:bat[:hge],false:bit);',
        'generator.projection(X_22=[0]:bat[:hge],X_19=[9801]:bat[:oid],X_13=[99]:bat[:hge]);',
    ]

    for obj, stmt in zip(objs, stmts):
        assert stmt == transformers.statement_constructor(loads(obj))['stmt']
