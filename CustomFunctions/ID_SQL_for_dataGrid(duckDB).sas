method dataGrid_SQL(
	varchar(50000) stmt
	, in_out package datagrid target_dataGrid
	, package datagrid dataGrid1
	, package datagrid dataGrid2
	, package datagrid dataGrid3
	, package datagrid dataGrid4
	) returns varchar;

	dcl double rc;
	dcl package pymas py;
	dcl double pystop;
	dcl package logger logr('App.tk.SID.Python');

	dcl nvarchar(10485760) pypgm;
	dcl varchar(500) retMsg;
	dcl double revision;
	
	dcl varchar(10485760) dataGrid1str;
	dcl varchar(10485760) dataGrid2str;
	dcl varchar(10485760) dataGrid3str;
	dcl varchar(10485760) dataGrid4str;
	
	retMsg= '';
	
	if NULL(dataGrid1) then
		dataGrid1str= '';
	else
		dataGrid1str= DATAGRID_TOSTRING(dataGrid1) ;

	if NULL(dataGrid2) then
		dataGrid2str= '';
	else
		dataGrid2str= DATAGRID_TOSTRING(dataGrid2) ;
		
	if NULL(dataGrid3) then
		dataGrid3str= '';
	else
		dataGrid3str= DATAGRID_TOSTRING(dataGrid2) ;

	if NULL(dataGrid4) then
		dataGrid4str= '';
	else
		dataGrid4str= DATAGRID_TOSTRING(dataGrid4) ;

	if null(py) and pystop ^= 1 then do;
		py = _new_ pymas();
		if inmas() then do;
			rc = py.useModule('"CODE_FILE_SCORE_py_1154797533"', 1);
		end;
		else do;
			rc = 1;
		end;
		if rc then do;
			rc = py.appendSrcLine('import pandas as pd');
			rc = py.appendSrcLine('import numpy');
			rc = py.appendSrcLine('import duckdb');
			rc = py.appendSrcLine('import json');
			rc = py.appendSrcLine('########################################################################################################');
			rc = py.appendSrcLine('def dgToDf(dg):');
			rc = py.appendSrcLine('    df_raw={}');
			rc = py.appendSrcLine('    numCols= range(len(dg[0][''metadata'']))');
			rc = py.appendSrcLine('    for col in numCols:');
			rc = py.appendSrcLine('        df_data= []');
			rc = py.appendSrcLine('        for data in dg[1][''data'']:');
			rc = py.appendSrcLine('            df_data.append(data[col])');
			rc = py.appendSrcLine('        df_raw[list(dg[0][''metadata''][col].keys())[0]]= df_data');
			rc = py.appendSrcLine('    df= pd.DataFrame(df_raw)');
			rc = py.appendSrcLine('    return(df)');
			rc = py.appendSrcLine('########################################################################################################');
			rc = py.appendSrcLine('def dfToDg(df):');
			rc = py.appendSrcLine('    #datagrid out columns');
			rc = py.appendSrcLine('    colsDf= list(df)');
			rc = py.appendSrcLine('    dgCols= []');
			rc = py.appendSrcLine('    for col in colsDf:');
			rc = py.appendSrcLine('        if str(df[col].dtypes) == ''object'':');
			rc = py.appendSrcLine('            colType= ''string''');
			rc = py.appendSrcLine('        elif str(df[col].dtypes) == ''int64'':');
			rc = py.appendSrcLine('            colType= ''int''');
			rc = py.appendSrcLine('        elif str(df[col].dtypes) == ''int32'':');
			rc = py.appendSrcLine('            colType= ''int''');
			rc = py.appendSrcLine('        elif str(df[col].dtypes) == ''float64'':');
			rc = py.appendSrcLine('            colType= ''decimal''');
			rc = py.appendSrcLine('        else:');
			rc = py.appendSrcLine('            colType= ''bool''');
			rc = py.appendSrcLine('        dgCols.append({col:colType})');
			rc = py.appendSrcLine('');
			rc = py.appendSrcLine('    #datagrid out rows (data)');
			rc = py.appendSrcLine('    dfJson= json.loads(df.to_json(orient = ''records''))');
			rc = py.appendSrcLine('    dgData= []');
			rc = py.appendSrcLine('    for r in range(len(dfJson)):');
			rc = py.appendSrcLine('        dgRow= []');
			rc = py.appendSrcLine('        for col in dfJson[r].keys():');
			rc = py.appendSrcLine('            dgRow.append(dfJson[r][col])');
			rc = py.appendSrcLine('        dgData.append(dgRow)');
			rc = py.appendSrcLine('');
			rc = py.appendSrcLine('    #write datagrid');
			rc = py.appendSrcLine('    dg= []');
			rc = py.appendSrcLine('    dg.append({''metadata'':dgCols})');
			rc = py.appendSrcLine('    dg.append({''data'':dgData})');
			rc = py.appendSrcLine('    ');
			rc = py.appendSrcLine('    return dg');
			rc = py.appendSrcLine('########################################################################################################');
			rc = py.appendSrcLine('');
			rc = py.appendSrcLine('def execute (dataGrid1,dataGrid2,dataGrid3,dataGrid4,stmt):');
			rc = py.appendSrcLine('    ''Output: dg, msg''');
			rc = py.appendSrcLine('');
			rc = py.appendSrcLine('    msg= ""');
			rc = py.appendSrcLine('    if dataGrid1 != None:');
			rc = py.appendSrcLine('        T1= dgToDf(json.loads(dataGrid1))');
			rc = py.appendSrcLine('    else:');
			rc = py.appendSrcLine('        T1= ""');
			rc = py.appendSrcLine('    if dataGrid2 != None:');
			rc = py.appendSrcLine('        T2= dgToDf(json.loads(dataGrid2))');
			rc = py.appendSrcLine('    else:');
			rc = py.appendSrcLine('        T2= ""');
			rc = py.appendSrcLine('    if dataGrid3 != None:');
			rc = py.appendSrcLine('        T3= dgToDf(json.loads(dataGrid3))');
			rc = py.appendSrcLine('    else:');
			rc = py.appendSrcLine('        T3= ""');
			rc = py.appendSrcLine('    if dataGrid4 != None:');
			rc = py.appendSrcLine('        T4= dgToDf(json.loads(dataGrid4))');
			rc = py.appendSrcLine('    else:');
			rc = py.appendSrcLine('        T4= ""');
			rc = py.appendSrcLine('    ');
			rc = py.appendSrcLine('    stmt= stmt.replace(";\n", " ")');
			rc = py.appendSrcLine('    try:');
			rc = py.appendSrcLine('        con= duckdb.connect("")');
			rc = py.appendSrcLine('        dfout= con.execute(stmt).df()');
			rc = py.appendSrcLine('    except Exception as err:');
			rc = py.appendSrcLine('        msg= str(err)');
			rc = py.appendSrcLine('        return "", msg');
			rc = py.appendSrcLine('        ');
			rc = py.appendSrcLine('    dg= json.dumps(dfToDg(dfout))');
			rc = py.appendSrcLine('');
			rc = py.appendSrcLine('    return dg, msg');
			pypgm = py.getSource();
			revision = py.publish(pypgm, '"CODE_FILE_SCORE_py_1154797533"');
			if revision < 1 then do;
				pystop = 1;
				logr.log( 'e', 'publish revision=$s', revision );
				return rc;
			end;
		end;
		else do;
			logr.log( 'd', 'useModule rc=$s', rc );
		end;
		rc = py.useMethod('execute');
		if rc then do;
			pystop = 1;
			logr.log( 'e', 'useMethod rc=$s', rc );
			return rc;
		end;
	end;
	if pystop ^= 1 then do;
		rc = py.setString ('dataGrid1', dataGrid1str);
		if rc then do;
			logr.log( 'e', 'set dataGrid1 rc=$s', rc );
			return rc;
		end;
		rc = py.setString ('dataGrid2', dataGrid2str);
		if rc then do;
			logr.log( 'e', 'set dataGrid2 rc=$s', rc );
			return rc;
		end;
		rc = py.setString ('dataGrid3', dataGrid3str);
		if rc then do;
			logr.log( 'e', 'set dataGrid3 rc=$s', rc );
			return rc;
		end;
		rc = py.setString ('dataGrid4', dataGrid4str);
		if rc then do;
			logr.log( 'e', 'set dataGrid4 rc=$s', rc );
			return rc;
		end;
		rc = py.setString ('stmt', stmt);
		if rc then do;
			logr.log( 'e', 'set stmt rc=$s', rc );
			return rc;
		end;
		rc = py.execute();
		if rc then do;
			logr.log( 'd', 'execute rc=$s', rc );
			return rc;
		end;
		DATAGRID_CREATE(target_dataGrid, py.getString('dg')) ;
        retMsg= py.getString('msg');
	end;
	return retMsg;
end;
