###############################################################
#The function generates random output from Champinon, Control Group and Challenger Groups
#At the first call a dictionary with random entries for the output groups is generated.
#The number of groups is based in the input parameters. 
#From second call on the output groups are taken from the generated dictionary.
#
#numRows is the number of records passed trough. From the number of records passed trough records will randomly be assigned to 
#the Control group and the Challenger groups according to the parameter numbers. These groups can be set to 0. 
#numRows needs to be bigger than Control and Challengers. 
#Records from numRows not assigned to Control or Challengers will be assigned to Champinon.
#If more records are passed trough than numRows abGroup will be set to N/A 
###############################################################
import secrets
import collections
import random
###############################################################
numRows=    50000 #number of records passed through - This number MUST be greater than Control and Challenger Groups!
numControl= 5000  #number of control records
numChall_1= 12000 #number of records for Challenger 1
numChall_2= 12000 #number of records for Challenger 2
numChall_3= 12000 #number of records for Challenger 3
numChall_4= 0     #number of records for Challenger 4
numChall_5= 0     #number of records for Challenger 5
###############################################################
abTestGroupsDic= {}
cnt= -1

def getABSplitGroupsPy(numRows,numControl,numChall_1,numChall_2,numChall_3,numChall_4,numChall_5):
    global abTestGroupsDic
    
    challList= [numChall_1, numChall_2, numChall_3, numChall_4, numChall_5]
    challName= ['Chall_1', 'Chall_2', 'Chall_3', 'Chall_4', 'Chall_5']

    #generate a list with idexes that we use as index for abTestGroupsDic{}. We ramdonly assign valuse to the indexes
    allRows= list(range(numRows))
    
    #set the rows for the control group
    maxRows= numRows-1
    for i in range(numControl):
        #generate random number in range. It will not generate dulicate numbers untill all numbers in the range are used.
        idx= random.randint(0,maxRows-i)
        abTestGroupsDic[allRows[idx]]= 'Ctrl'
        del allRows[idx]        
    
    #set the rows for the challenger group. We subtract the number of challenger as we have gebnerated them already
    maxRows= numRows-numControl-1
    #print(maxRows)
    #print(len(allRows))
    challNameIdx= 0
    for chall in challList:
        for c in range(chall):
            idx= random.randint(0,maxRows-c)
            abTestGroupsDic[allRows[idx]]= challName[challNameIdx]
            del allRows[idx]        
        challNameIdx+= 1
        #set new max rows. We only do this if the challenger is greater than 0. (if not all challengers are used!)
        if chall > 0:
            maxRows= maxRows-c-1
            c= 0
   
    #set the rows for the champion group. These are the remaining slots from allRows that we have not used yet.
    for i in allRows:
        abTestGroupsDic[i]= 'Champ'
        
    return
    
def execute():
    'Output:abGroup'

    global cnt
    global abTestGroupsDic

    if len(abTestGroupsDic) == 0:
        #numRow needs to be greater than all Control and Chall!
        if numRows < (numControl + numChall_1 + numChall_2 + numChall_3 + numChall_4 + numChall_5):
            return 'Error: numRows too small!', cnt

        getABSplitGroupsPy(int(numRows),int(numControl),int(numChall_1),int(numChall_2),int(numChall_3),int(numChall_4),int(numChall_5))
    cnt+= 1
    try:
        abGroup= abTestGroupsDic[cnt]
    except:
        abGroup= 'N/A'
    return abGroup, cnt
    
    
    