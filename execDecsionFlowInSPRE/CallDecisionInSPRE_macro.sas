/******************************************************/
/*Create macro and store macro in dataset             */
/*We can then call the macro from the dataset         */
/******************************************************/
proc options
	option= MSTORED;
run;

/*library to store macro */
%if (%sysfunc(libref(MACROS))) %then %do;
	libname macros '/opt/sas/spre/config/etc/macros';
	options mstored sasmstore=macros;
%end;

%macro DCM_EXECUTE_DECISION_SPRE(URI=, inputTable=, outputTable=, libs= ) / store;
	options nonotes;
	proc ds2;
	ds2_options sas;
	package generateSPRECode /inline;
		dcl package pymas py;
		dcl double pystop revision;
		dcl package logger logr('App.tk.MAS');
		dcl nvarchar(10485760) pypgm;
		dcl int sourceLoaded;
	/****************************************************************************************************/
	/* Load the Python code                                                                   */
	/****************************************************************************************************/
		method loadSource() returns double;
			pystop= 0;
			if null(py) and pystop ^= 1 then do;
				py= _new_ pymas();
				py.appendSrcLine('import sys');
				/* The insert path need to point where the file get_decision_code_SPRE.py is! */
				py.appendSrcLine('sys.path.insert(0, ''/etc/sas/dec-spre/app'')');
				py.appendSrcLine('import get_decision_code_SPRE as dc');
				py.appendSrcLine('def execute(uri, input_table, output_table, libs):');
				py.appendSrcLine('    ''Output: fileName''');
				py.appendSrcLine('    decisionCode= dc.decisionSPRECode()');
				py.appendSrcLine('    decisionCode.setDecisionInfo(uri, input_table, output_table, libs)');			
				py.appendSrcLine('    decisionCode.getAccessToken()');
				py.appendSrcLine('    decisionCode.getDecisionName()');
				py.appendSrcLine('    decisionCode.getDecisionCode()');
				py.appendSrcLine('    decisionCode.setProcDs2()');
				py.appendSrcLine('    decisionCode.modifyContactRecord()');
				py.appendSrcLine('    decisionCode.getDecisionParameters()');
				py.appendSrcLine('    decisionCode.prepareParameters()');
				py.appendSrcLine('    fileName= decisionCode.writeDecisionCode()');
				py.appendSrcLine('    return fileName');
				pypgm = py.getSource();
				revision = py.publish(pypgm, 'thedqcode');
				if revision < 1 then do;
					pystop = 1;
					logr.log( 'e', 'publish revision=$s', revision );
					return pystop;
				end;
				sourceLoaded= 1;
			end;
			return pystop;
		end;
	/****************************************************************************************************/
	/* Call the Python code                                                                   */
	/****************************************************************************************************/
		method generateDecisionCode(varchar(500) uri, varchar(50) input_table, varchar(50) output_table, varchar(100) libs, in_out varchar codeFile);
			dcl int rc;
			if missing(sourceLoaded) then
				loadSource();
	
			rc= py.useMethod('execute');
			if rc then do;
				pystop= 1;
				logr.log( 'e', 'useMethod execute: rc=$s', rc );
			end;
	
			if pystop ^= 1 then do;
				rc= py.setString('uri', uri);
				rc= py.setString('input_table', input_table);
				rc= py.setString('output_table', output_table);
				rc= py.setString('libs', libs);
				rc= py.execute();
				codeFile= py.getString('fileName');
				logr.log( 'd', 'execute rc=$s', rc);
			end;
		end;
	endpackage;
	/****************************************************************************************************/
	/*Call decision flow through the ds2 apckage                                                        */
	/****************************************************************************************************/
	data work.dcmfile (overwrite=yes);
	    dcl package generateSPRECode dcf();
	    dcl varchar(500) uri codeFile; 
	    dcl varchar(50) input_table output_table;
	    dcl varchar(100) libs;
	    method run();
	        uri= %tslit(&URI);
		    input_table= %tslit(&inputTable);
	    	output_table= %tslit(&outputTable);
	    	libs= %tslit(&libs);
			dcf.generateDecisionCode(uri, input_table, output_table, libs, codeFile);	
	        end;
	    run;
	quit;
	
	/*get the decision ds2 code file name */
	data _null_;
		set work.dcmfile;
		call symputx("CODEFILE", codeFile);
	run;
	
	/* delete tmp dataset */
	proc datasets lib=work nolist;
		delete dcmfile;
	run;

	/*include the decision code and execute the decision */
	options noquotelenmax;
	filename deccode %tslit(&CODEFILE);
	%include deccode;
%mend DCM_EXECUTE_DECISION_SPRE;

