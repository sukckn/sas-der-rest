#!/opt/sasinside/anaconda3/bin/python
# -*- coding: utf-8 -*-
#
#loadIDCustomFunction.py
#January 2021
#
#load/update custom function into SAS Intelligen Decisioning
#The script will load a new custom function into ID. If the function exists already it will update the funcion.
#If the category does not exist it will be created.
#The function will be passed into the script via a file
#The file has three sections
#category:
#<name of the ID categroy for the function>
#description:
#<function description>
#code:
#function ds2 code
########################################################################################################
import argparse
import sys
import os
import json
from os.path import expanduser
sys.path.insert(0, "/etc/sas/pycode")
import loadCustomFunction as lcf
    
#########################################################################################################
def getServer():
    home= expanduser("~")
    confFileName= home +'/.sas/config.json'
    try:
        confFile= open(confFileName, 'r')
        conf= confFile.read()
        confFile.close()
    except:
        print("\nCan't find CLI profile. Please run: 'sas-admin profile init'")
        quit()

    try:
        server= json.loads(conf)['Default']['sas-endpoint']
    except:
        print("\nCan't find sas-endpoint. Please run: 'sas-admin profile init'")
        quit()
    return server[server.find(':')+3:]
    
#########################################################################################################
def getAccessToken():
    home= expanduser("~")
    credentialsFileName= home +'/.sas/credentials.json'
    try:
        credentialsFile= open(credentialsFileName, 'r')
        credentials= credentialsFile.read()
        credentialsFile.close()
    except:
        print("\nCan't find login token. Please run: 'sas-admin auth login'")
        quit()

    try:
        token= json.loads(credentials)['Default']['access-token']
    except:
        print("\nCan't find login token. Please run: 'sas-admin auth login'")
        quit()
    
    return token
####################################################################
def readCustomFunction(fileName):
    try:
        f= open(fileName , 'r')
    except:
        print("\nCannot open file: " + fileName)
        quit()
        
    customFunction= f.readlines()
    f.close()

    category= ''
    isCategory= False
    description= ''
    isDescription= False
    code= ''
    isCode= False
    for line in customFunction:       
        if 'category:' in line.lower().strip():
            isCategory= True
            continue
        if isCategory:
            category= line.strip()            
            isCategory= False
        
        if  'description:' in line.lower().strip():
            isDescription= True
            continue
        if isDescription:
            if  'code:' in line.lower().strip():
                isDescription= False
                isCode= True
                continue
            description+= line.lstrip()
            
        if isCode:
            code+= line    
            
    functionName= code[code.lower().find('method'):code.lower().find('(')].strip()
    
    #Check if Category, functionName and code is not empty
    if len(category) == 0:
        print("Could not find category name in custom function file!")
        quit()
    if len(code) == 0:
        print("Could not find code in custom function file!")
        quit()
    if len(functionName) == 0:
        print("Could not find function name in custom funcion code!")
        quit()
          
    return category, description, code, functionName

####################################################################
def loadCustomFunction(code, description, categoryName, server, token, logLevel=0, logOut=False):
    
    loadFunc= lcf.loadCustomFunction(logFileName="loadCustomFunction.log", logDir="/tmp")
    loadFunc.setStdout(logOut)
    loadFunc.setLogLevel(logLevel)
    loadFunc.setViyaConnectInfo(token=token)
    #create category if it does not exist
    loadFunc.createCategory(categoryName)
    #we create the function if not there otherwise we update it
    loadFunc.getFunctionInfo(code)
    funcId= None
    message= ""
    if len(loadFunc.custFuncId)  == 0:
        funcId= loadFunc.createFunction(code, description)
        message= "Created custom function: " + loadFunc.funcName
    else:
        funcId= loadFunc.updateFunction(code, description)
        message= "Updated custom function: " + loadFunc.funcName    
    
    if funcId == None:
       message= "Error creating/updating custom function. Check log file " + logDir + "/" + logFileName
    return message

#########################################################################################################
def getInputArguments():
    parser = argparse.ArgumentParser(prog="loadIDCustomFunction",
                                     description="Loads or updates a custom function into SAS Intelligent Decisioning.")
    parser.add_argument("--file","-f",  help="Specifies the file containing custom function information.",required='True')
    parser.add_argument("--logLevel","-ll",  type=int, help="Specifies the log level between 0 (default) and 5. The higher the level the more information is written to the log.", default=0, choices=[0,1,2,3,4,5])
    parser.add_argument("--logOut","-lo",  help="Controls where to write the log information. If set it writes log information to the logfile and to the comand line.", action="store_true")
    args = parser.parse_args()

    fileName= args.file
    logLevel= args.logLevel   
    logOut= args.logOut
    
    return fileName, logLevel, logOut

####################################################################
def main():
    fileName, logLevel, logOut= getInputArguments()
    access_token= getAccessToken()
    server= getServer()

    category, description, code, functionName= readCustomFunction(fileName)
    
    msg= loadCustomFunction(code, description, category, server, access_token, logLevel, logOut)

    print(msg +" in category: " +category +".")

    return
####################################################################
if __name__ == "__main__":
    main()
    
    
    