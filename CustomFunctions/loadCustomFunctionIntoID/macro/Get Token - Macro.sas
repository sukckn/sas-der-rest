proc options
	option= MSTORED;
run;

/*library to store macro */
%if (%sysfunc(libref(MACROS))) %then %do;
	options mstored sasmstore=macros;
	libname macros '/var/sas_projects/latvia/belfius/macros';
%end;

%macro VIYA_TOKEN(TOKEN=) / store;
	%let VIYA_TOKEN_username= sasadm;
	%let VIYA_TOKEN_password= Go4thsas;
	%let VIYA_TOKEN_clientIDsecret= YXBwOk15U3VwZXJTZWNyZXRQdw==;
	%let VIYA_TOKEN_server= viyacloud.westeurope.cloudapp.azure.com;
		
	/* Get Viya Access Token */
	filename tok temp;
	proc http url="https://&VIYA_TOKEN_server/SASLogon/oauth/token"
	   in="grant_type=password%nrstr(&username)=&VIYA_TOKEN_username%nrstr(&password)=&VIYA_TOKEN_password"
	   out=tok;
	   headers "Content-Type"="application/x-www-form-urlencoded"
	   "Authorization"="Basic &VIYA_TOKEN_clientIDsecret";
	run;
	
	libname acctok json fileref=tok;
	data _null_;
	 set acctok.root;
	 %global &TOKEN;
	 call symputx("&TOKEN",access_token);
	run;
%mend VIYA_TOKEN;
