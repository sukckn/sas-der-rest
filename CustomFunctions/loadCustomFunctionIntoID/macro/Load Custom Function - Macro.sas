proc options
	option= MSTORED;
run;

/*library to store macro */
%if (%sysfunc(libref(MACROS))) %then %do;
	options mstored sasmstore=macros;
	libname macros '/var/sas_projects/latvia/belfius/macros';
%end;

%macro DCM_LOAD_CUSTOM_FUNCTION(FunctionDir=, FunctionFile=) / store;
options nonotes;

filename ndgfld filesrvc folderPath=&FunctionDir;

data work.nesteddg;
	infile ndgfld(&FunctionFile) LRECL=200 pad;
	length line $200;
	input line $200.;
run;

proc ds2;
data _NESTEDDG (overwrite=yes);
	dcl varchar(50) lineType;
	retain lineType;
	method run();
		set NESTEDDG;	
		if lowcase(strip(line)) = 'category:' then do;
			lineType= 'category';
		end;
		if lowcase(strip(line)) = 'description:' then do;
			lineType= 'description';
		end;
		if lowcase(strip(line)) = 'code:' then do;
			lineType= 'code';
		end;
	end;
enddata;
run;
quit;

proc ds2;
data NESTEDDG (overwrite=yes keep= (lineType value));
	dcl varchar(5000) value descBuffer codeBuffer;
	retain descBuffer codeBuffer;
	method run();
		set _NESTEDDG; 
		if lowcase(strip(lineType)) = 'category' and lowcase(strip(line)) ^= 'category:' and length(line) > 0 then do;			
			value= substrn(line,notspace(line));
			output;
			value= '';
		end;

		if lowcase(strip(lineType)) = 'description' and lowcase(strip(line)) ^= 'description:' and length(line) > 0 then do;			
			descBuffer= cat(descBuffer, trim(substrn(line,notspace(line))), '\n');
		end;

		if lowcase(strip(lineType)) = 'code' and lowcase(strip(line)) ^= 'code:' and length(line) > 0 then do;			
			codeBuffer= cat(codeBuffer, trim(line), '\n');
		end;
	end;

	method term();
		lineType= 'description';
		value= descBuffer;
		output;
		lineType= 'code';
		value= codeBuffer;
		output;
	end;
enddata;
run;
quit;

data _null_;
	set NESTEDDG;
	if lineType = 'category' then do;
		value= strip(value);
		call symputx("categoryName",value);
	end;

	if lineType = 'description' then do;
		value= strip(value);
		call symputx("description",value);
	end;

	if lineType = 'code' then do;
		value= strip(value);
		call symput("code",value);
	end;
run;

proc ds2 ;
	data _null_;
	
	dcl package pymas py;
	dcl int sourceLoaded;
	dcl nvarchar(10485760) pycode;
	dcl varchar(10) checkFlag;
	
		method loadPySource();
			py= _new_ pymas();
			
			py.appendSrcLine('import sys');
			py.appendSrcLine('sys.path.insert(0, "/var/sas_projects/latvia/belfius/python/src")');
			py.appendSrcLine('import loadCustomFunction as lcf');
			py.appendSrcLine('def loadCustomFunction(code, description, categoryName, token=""):');
			py.appendSrcLine('    "Output: message"');
			py.appendSrcLine('    ');
			py.appendSrcLine('    loadFunc= lcf.loadCustomFunction(logFileName="loadCustomFunction.log", logDir="/var/sas_projects/latvia/belfius/python/tmp")');
			py.appendSrcLine('    loadFunc.setStdout()');
			py.appendSrcLine('    loadFunc.setLogLevel(0)');
			py.appendSrcLine('    loadFunc.setViyaConnectInfo(server="viyacloud.westeurope.cloudapp.azure.com", token=token)');
			py.appendSrcLine('    #create category if it does not exist');
			py.appendSrcLine('    loadFunc.createCategory(categoryName)');
			py.appendSrcLine('    #we create the function if not there otherwise we update it');
			py.appendSrcLine('    loadFunc.getFunctionInfo(code)');
			py.appendSrcLine('    funcId= None');
			py.appendSrcLine('    message= ""');
			py.appendSrcLine('    if len(loadFunc.custFuncId)  == 0:');
			py.appendSrcLine('        funcId= loadFunc.createFunction(code, description)');
			py.appendSrcLine('        message= "Created custom function: " + loadFunc.funcName');
			py.appendSrcLine('    else:');
			py.appendSrcLine('        funcId= loadFunc.updateFunction(code, description)');
			py.appendSrcLine('        message= "Updated custom function: " + loadFunc.funcName    ');
			py.appendSrcLine('    ');
			py.appendSrcLine('    if funcId == None:');
			py.appendSrcLine('       message= "Error creating/updating custom function. Check log file " + logDir + "/" + logFileName');
			py.appendSrcLine('    return message');
			
			pycode= py.getSource();
			py.publish(pycode, 'idloadcustomfunction');		
		end;
		method run();
			dcl varchar(10000) code token; 
			dcl varchar(500) description categoryName message;
			code= %tslit(&code);

			description= %tslit(&description); 
			categoryName= %tslit(&categoryName); 
			token=%tslit(&idtoken);
			
			if missing(sourceLoaded) then
				loadPySource();			
			py.useMethod('loadCustomFunction');
			py.setString('code', code);
			py.setString('description', description);
			py.setString('categoryName', categoryName);
			py.setString('token', token);

			py.execute();
			
			message= py.getString('message');
			put message=;
		end;
	enddata;
run;quit;
%mend DCM_LOAD_CUSTOM_FUNCTION;

