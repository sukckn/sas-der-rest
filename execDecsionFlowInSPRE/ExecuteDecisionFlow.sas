/*macro library */
%if (%sysfunc(libref(MACROS))) %then %do;
	libname macros '/opt/sas/spre/config/etc/macros';
	options mstored sasmstore=macros;
%end;

/*get the revision URI */
%DCM_GET_REVISIONS(TYPE=DECISION, 
				   FILTER=eq(name, 'monitorTruck'), 
                   TABLE=casuser.rev, PROMOTE=NO);

/*set revision URI for revision 1.0 */
data _null_;
	set CASUSER.REV;
	where majorRevision = 1 and minorRevision = 0;
	CALL SYMPUT('URI',revisionURI);
	put revisionURI=;
run;

/*Set database connection and execute decision flow */
libname PGDATA postgres server=localhost port=5433 user=sas password='Orion123' database=postgres schema=PGDATA;
%DCM_EXECUTE_DECISION_SPRE(URI= &URI,
						   INPUTTABLE= work.test_truck,
						   OUTPUTTABLE= work.test_truck_out,
						   LIBS= PGDATA);
