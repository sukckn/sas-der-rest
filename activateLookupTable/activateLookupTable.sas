%macro activateLookupTable(lookupTableName);
/*%let lookupTableName= Invalid_Name_Values;*/
	/* get the local server name */
	data _null_;
		call symput('server', substr("&_baseurl", 1, prxmatch("\/SASStudio/\", "&_baseurl") - 1));
	run;
	/* set URL to get lookup table ID */
	data _null_;
		url= cat('"', "&server", '/referenceData/domains?filter=eq(name,%tslit(&', 'lookupTableName))', '"');
		call symputx('url', url);
		put url=;
	run;
	
	/* call REST API to get lookup table ID */
	filename lpinfo temp;
	proc http
		method= "GET"   	
		url= &url
		out= lpinfo
	    oauth_bearer= sas_services;
	 	headers 
	    	"Content-Type"="application/json";
	run;		
	
	/***********************************************************************************************************/
	
	/* read lookup table ID */
	libname lpinfo json fileref=lpinfo;
	data _null_;
		set LPINFO.ITEMS;
		call symput("lookupId", ID);
		put ID=;
	run;
	
	/* set URL to get ETag for lookup table ID */
	data _null_;
		url= cat('"', "&server", '/referenceData/domains/&lookupId/currentContents', '"');
		call symputx('url', url);
		put url=;
	run;
	
	/* call REST API to get ETag lookup table ID */
	filename hdinfo temp;
	proc http
		method= "GET"   	
		url= &url
		headerout= hdinfo
	    oauth_bearer= sas_services;
	 	headers 
	    	"Content-Type"="application/json";
	run;		
	
	/* read ETag. We need it to activate the lookup table */
	data _null_;
		infile hdinfo;
		length buffer ETag $100;
		input; 
		buffer= strip(_infile_);
		idx= index(buffer, "ETag:");
		if idx > 0 then do;
			ETag= substr(buffer, 6);
			call symputx('ETag', ETag);
			put ETag=;		
		end;
	run;
	
	/***********************************************************************************************************/
	/* activate lookup table for CAS*/
	proc http
		method= "PATCH"   	
		url= &url
		in= '[{"op": "copy","from": "/@current", "path": "/@current/environments/cas"}]'
	    oauth_bearer= sas_services;
	 	headers 
	    	'Content-Type'='application/json'
			'If-Match'= %tslit(&ETag);
	run;
	%put Activated ==> &lookupTableName;
%mend activateLookupTable;

%activateLookupTable(Invalid_Name_Values);
%activateLookupTable(UK_Counties);
%activateLookupTable(Person Titles);
%activateLookupTable(IBAN_Length);
%activateLookupTable(DQ_Dimensions_Weight);
%activateLookupTable(DQ_Dimensions_Mapping);


