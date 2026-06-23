data work.country;
	length country $30;
	infile cards;
	input country $;
	cards;
USA
United Kingdom
Germany
South Africa
Canada
France
Italy
Spain
;
run;

data work.address;
	length address town country $30;
	infile cards dlm=",";
	input address town country $;
	cards;
Oppelner Strasse 12,Marl,Germany
2 Trowley Hill Rd,Flamstead,UK
10 Chiswell St,London,UK
333 Orchard Rd,Singapore,
;
run;

data work.postcodes;
	length po1-po03 $10;
	infile cards dlm=",";
	input po1 po2 po3 $;
	cards;
AL3 8EE,AL4 0RQ,W2 1JU
OX49 5NU,M32 0JG,NE30 1DP
;
run;

data postcodes_2;
	length postcode $10;
	infile cards dlm=",";
	input postcode $ test $;
	cards;
AL3 8EE,a'aa
AL4 0RQ,a"aa
W2 1JU,aaa
OX49 5NU,aaa
M32 0JG,aaa
NE30 1DP,aaa
NE"30 1DP,aaa
NE'30 1DP,aaa
;
run;

%let viyaHost= %sysfunc(getoption(SERVICESBASEURL));

proc http
	method= "POST"
	url= "&viyaHost./referenceData/globalVariables"
	in= '{"name": "httpRequest","dataType": "string", "defaultValue": "Step"}'
	oauth_bearer= sas_services;
	headers
		'Accept'='application/json'
		'Content-Type'='application/json';
quit;

%symdel viyaHost;
