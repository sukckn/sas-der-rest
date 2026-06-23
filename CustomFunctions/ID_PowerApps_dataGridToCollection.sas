method dataGridToCollection(in_out varchar dgRaw) returns varchar;
  dcl package pymas py;
  dcl double pystop;
  dcl package logger logr('App.tk.MAS');
  dcl nvarchar(10485760) pypgm;
  dcl nvarchar(32000) collection;
  dcl double rc;
  dcl double revision;
  dcl nvarchar(100) pyFile;
  
  pyFile= '"dataGridToCollection_2109001344"';
  
  if null(py) and pystop ^= 1 then do;
    py= _new_ pymas();
    if inmas() then do;
        rc= py.useModule(pyFile, 1);
    end;
    else do;
        rc= 1;
    end;
    if rc then do;
/***********************************************************************************************************/    
/* Python Code */
      py.appendSrcLine('import json');
      py.appendSrcLine('def dataGridToCollectionPy (dgRaw):');
      py.appendSrcLine('    ''Output:collection''');
      py.appendSrcLine('    dgRaw= dgRaw.replace(''\\"'', ''"'')');      
      py.appendSrcLine('    dg= json.loads(dgRaw)');
      py.appendSrcLine('');
      py.appendSrcLine('    columns= []');
      py.appendSrcLine('    for col in dg[0][''metadata'']:');
      py.appendSrcLine('        columns.append(*col)');
      py.appendSrcLine('');
      py.appendSrcLine('    collection= []');
      py.appendSrcLine('    columnCnt= len(columns)');
      py.appendSrcLine('    for row in dg[1][''data'']:');
      py.appendSrcLine('        collectionRow= {}');
      py.appendSrcLine('        for i in range(columnCnt):');
      py.appendSrcLine('            collectionRow[columns[i]]= row[i]');
      py.appendSrcLine('        collection.append(collectionRow)');
      py.appendSrcLine('    return ":dg:" +json.dumps(collection)');
/***********************************************************************************************************/
/* publish Python code to file in order to execute it */
      pypgm= py.getSource();
      revision= py.publish(pypgm, pyFile);
      if revision < 1 then do;
        pystop= 1;
        logr.log( 'e', '$s: publish revision=$s', pyFile, revision );
        return '';
      end;
    end;
    else do;
      logr.log( 'd', '$s: useModule rc=$s', pyFile, rc );
    end;
/***********************************************************************************************************/  
/* set the Python function bto be executed */
    rc= py.useMethod('dataGridToCollectionPy');
    if rc then do;
      pystop = 1;
      logr.log( 'e', '$s: useMethod rc=$s', pyFile, rc );
      return '';
    end;
  end;
/***********************************************************************************************************/    
/* set parameters for Python function */
  if pystop ^= 1 then do;
    rc= py.setString ('dgRaw', dgRaw);
    if rc then do;
      logr.log( 'e', '$s: set dgRaw rc=$s', pyFile, rc );
      return '';
    end;
/***********************************************************************************************************/      
/* execute Pytghon function */
    rc = py.execute();
    logr.log( 'd', '$s: execute rc=$s', pyFile, rc );
/***********************************************************************************************************/     
/* get return parameters from Python function */
    collection= py.getString('collection');
  end;
  
  return collection;
end;

