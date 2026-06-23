package "${PACKAGE_NAME}" /inline;
	dcl varchar(10485760) testRows;
    dcl int rowNum;
    dcl int numRows;
    
    method initABGroups();
	    dcl int numControl numChall_1 numChall_2 numChall_3 numChall_4 numChall_5;
	    dcl int i;
		
	    /* set the input parameters for the AB split group */
	    numRows= 46720;
	    numControl= numRows * 0.1; /* 10% */
	    numChall_1= 3000;
	    numChall_2= 3000;
	    numChall_3= 3000;
	    numChall_4= 0;
	    numChall_5= 0;
	    
	    /* split into random groups besed on input parameters */
	    testRows= getABSplitGroups(numRows, numControl, numChall_1, numChall_2, numChall_3, numChall_4, numChall_5);
    
		/* indicate that we have set the AB groups as we only what to do this once. This is also the counter for calling this ID node*/
        rowNum= 0;
    end;

    method execute(in_out varchar abGroup);
    	/* initilize AB groups at the first all */
    	if missing(rowNum) then
    		initABGroups();
    	
    	/* set the AB group for the calling record */
    	rowNum= rowNum+1;
    	if rowNum > numRows then
    		abGroup= 'Champ';
    	else
    		abGroup= scan(testRows, rowNum);
    end;
endpackage;