%let token= 'eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vbG9jYWxob3N0L1NBU0xvZ29uL3Rva2VuX2tleXMiLCJraWQiOiJsZWdhY3ktdG9rZW4ta2V5IiwidHlwIjoiSldUIn0.eyJqdGkiOiIxNWQxMmM1YzcwZTk0NThlODg5ODZmOGFiMjU4ODI3MSIsImV4dF9pZCI6InVpZD1zYXNkZW1vLG91PXVzZXJzLGRjPXZpeWFkZW1vLGRjPWNvbSIsInN1YiI6ImNiMTE3NWI4LWIwZGYtNDgyMS1iMGZjLTk3MTQyODE1NzIyYSIsInNjb3BlIjpbImNsaWVudHMucmVhZCIsInN2aXVzcnMiLCJjbGllbnRzLnNlY3JldCIsInVhYS5yZXNvdXJjZSIsIm9wZW5pZCIsInVhYS5hZG1pbiIsImNsaWVudHMuYWRtaW4iLCJzY2ltLnJlYWQiLCJzdmlhZG1zIiwiU0FTQWRtaW5pc3RyYXRvcnMiLCJjbGllbnRzLndyaXRlIiwic2NpbS53cml0ZSIsIkNBU0hvc3RBY2NvdW50UmVxdWlyZWQiXSwiY2xpZW50X2lkIjoic2FzLmVjIiwiY2lkIjoic2FzLmVjIiwiYXpwIjoic2FzLmVjIiwiZ3JhbnRfdHlwZSI6InBhc3N3b3JkIiwidXNlcl9pZCI6ImNiMTE3NWI4LWIwZGYtNDgyMS1iMGZjLTk3MTQyODE1NzIyYSIsIm9yaWdpbiI6ImxkYXAiLCJ1c2VyX25hbWUiOiJzYXNkZW1vIiwiZW1haWwiOiJzYXNkZW1vQG5vbmUuc2FzLmNvbSIsImF1dGhfdGltZSI6MTYwNjgxMTMxNiwicmV2X3NpZyI6IjI5NDIyM2RjIiwiaWF0IjoxNjA2ODExMzE2LCJleHAiOjE2MDY4NDczMTYsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3QvU0FTTG9nb24vb2F1dGgvdG9rZW4iLCJ6aWQiOiJ1YWEiLCJhdWQiOlsic2NpbSIsImNsaWVudHMiLCJzYXMuKiIsInVhYSIsIm9wZW5pZCIsInNhcy5lYyJdfQ.lrSjRxCi1rSAbsDInRCGtAFbMNiSqOp_ifuDY0N_Q4SSdislEkZOha4KFH71h_BUqzR92jyZDCZ4yc5u-WaRTy25NT9G4qF3NErEcY1sZ-DI3AG-vzQtzZWthaKGLn6tWIUP1GWT9FURXPZV60OnxA9qaxrGLq1MA10z_0zLn_I8egywdNLj71I9kJV5Odx910oxPxjzXySO9FZq0QVXuQatX2eSB5o4GvHlOV4D8U_ND7MKExg5GmBT2hkHbBY-4O84vHesWZrrUa3q89t8N2uvOFCiVPtSI7PUD_4DBr5FOC8F9xUaYQmqADP7iMamxQu34kWFTp_GeOxRxmMszA';
%let code= 'method QQQ();end;';
%let description= '';
%let categoryName= 'ASD';

proc ds2 sessref=mySession;
	data _null_;
	
	dcl package pymas py;
	dcl int sourceLoaded;
	dcl nvarchar(10485760) pycode;
	dcl varchar(10) checkFlag;
	
		method loadPySource();
			py= _new_ pymas();
			
			py.appendSrcLine('import sys');
			py.appendSrcLine('sys.path.insert(0, "/etc/sas/pycode")');
			py.appendSrcLine('import loadCustomFunction as lcf');
			py.appendSrcLine('def loadCustomFunction(code, description, categoryName, token=""):');
			py.appendSrcLine('    "Output: message"');
			py.appendSrcLine('    ');
			py.appendSrcLine('    loadFunc= lcf.loadCustomFunction(logFileName="loadCustomFunction.log", logDir="/tmp")');
			py.appendSrcLine('    loadFunc.setStdout()');
			py.appendSrcLine('    loadFunc.setLogLevel(4)');
			py.appendSrcLine('    loadFunc.setViyaConnectInfo(token=token)');
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
			code= &code;
			description= &description; 
			categoryName= &categoryName; 
			token= &token;
			
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




