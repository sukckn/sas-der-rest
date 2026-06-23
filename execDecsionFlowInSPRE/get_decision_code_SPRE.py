import requests
import base64
import json
import sys 
import os
import re
################################################################################
class decisionSPRECode:
    #these variables need to get adjusted for the environment where the code is executed
    server= '127.0.0.1'             #Viya server IP address          
    uid= 'sasdemo'                  #User to logon to Viya
    pwd= 'Orion123'                 #User password
    clientId= 'mas.client'          #Client Id needed to get access_token to call Viya web services
    clientSecret= 'Orion123'        #Client Secret needed to get access_token to call Viya web services
    codeDir= '/etc/sas/dec-spre/dec-ds2code'   #Linux directory where the decision code ds2 file is stored
    logDir= '/tmp'                  #Linux directory where log file is written, if error occurs
    
    ################################################################################
    artefactID= ''
    sasLibs= ''
    input_table= ''
    output_table= ''  
    decision_name= 'dcm'
    codeFile= ''
    token= ''
    decisionCode= []
    parameterList= []
    outputParaKeep= 'keep '
    outputParaDcl= []
    outDataGridList= []
    
    ################################################################################
    #get token to call ID Web Service
    ################################################################################
    def setDecisionInfo(self, uri, input_table, output_table, libs):
        
        self.input_table= input_table
        self.output_table= output_table
        
        #if libs was not set at input it will be None
        if libs == None:
            self.sasLibs+= ' WORK '
        else:
            self.sasLibs= ' ' +libs.upper() + ' '
        #make sure that work is always there
        if self.sasLibs.find(' WORK ') < 0:
            self.sasLibs+= ' WORK '
            
        if uri[len(uri)-1] == '/':
            uri= uri[0:len(uri)-1]
        self.uri= uri
            
        return

    ################################################################################
    #get token to call ID Web Service
    ################################################################################
    def log(self, msg):
        #also print out here when testing from command line
        print(msg)
        log= open(self.logDir +"/get_decision_code_SPRE.log", "a")
        log.write(str(msg)+'\n')
        log.close()
        
        return

    ################################################################################
    #get token to call ID Web Service
    ################################################################################
    def getAccessToken(self):
        loginCredentials={"grant_type":"password","username":self.uid,"password":self.pwd}
        appBinding= self.clientId + ':' + self.clientSecret
        appBinding64= base64.b64encode(bytes(appBinding, 'utf-8'))
        url= "http://%s/SASLogon/oauth/token" % (self.server)

        headers = {"Content-Type":"application/x-www-form-urlencoded", "Authorization":"Basic "}
        headers["Authorization"]= "Basic " + appBinding64.decode('ascii') #appBinding64 is type bytes but need to convert to type str
        response = requests.post(url, headers=headers, data=loginCredentials)

        if response.status_code < 200 or response.status_code >= 300:
            self.log('Error receiving user token!')
            self.log([response.json()])
            sys.exit()
        
        self.token= response.json()['access_token']
                
        return 

    ################################################################################
    #get Decision name
    ################################################################################
    def getDecisionName(self):
        url= "http://%s%s" % (self.server, self.uri)
        
        headers = {"Content-Type":"application/json", "Authorization":"Bearer "}
        headers["Authorization"]= "Bearer " + self.token
        response = requests.get(url, headers=headers)

        if response.status_code < 200 or response.status_code >= 300:
            self.log('Error calling MAS service!')
            self.log(response.json()['message'])
            self.log(response.json()['details'])
            self.log(url)
            sys.exit()

        self.decision_name= response.json()['name']
        self.artefactID= response.json()['id']
        
        return

    ################################################################################
    #get Decision code and save it in temp file
    ################################################################################
    def getDecisionCode(self):
        url= "http://%s%s/code?codeTarget=MICROANALYTICSERVICE&lookupMode=inline&isGeneratingRuleFiredColumn=false&rootPackageName=%s" % (self.server, self.uri, self.decision_name)
                
        headers = {"Content-Type":"text/vnd.sas.source.ds2", "Authorization":"Bearer "}
        headers["Authorization"]= "Bearer " + self.token
        response = requests.get(url, headers=headers)

        if response.status_code < 200 or response.status_code >= 300:
            self.log('Error calling MAS service!')
            self.log(response.json()['message'])
            self.log(response.json()['details'])
            self.log(url)
            sys.exit()

        self.decisionCode= response.text.split('\n')
        
        return

    ################################################################################
    #add PROC DS2 statement
    ################################################################################
    def setProcDs2(self):
        #add PROC DS2 statement
        self.decisionCode.insert(0, 'proc ds2 libs=(' +self.sasLibs +');')

        return
        
    ################################################################################
    #modify the calls to record contact to output from decision flow (as this is what we do for batch)
    ################################################################################
    def modifyContactRecord(self):
        for idx, line in enumerate(self.decisionCode):          
            #remove code to call record contact node and change statement to output record to create it later
            if line.find('st.recordContactHistory') >= 0:
                self.decisionCode[idx]= line[line.find('(')+1:line.find(',')] +'= ' +line[line.find(',')+1:line.find(')')] +';'
            elif line.strip() == 'dcl package masstate st();':
                self.decisionCode[idx]= ''
                
        return
        
    ################################################################################
    #get the parameters from the execute() method for the decision flow
    ################################################################################
    def getDecisionParameters(self):
        #identify last package as we need the root package later
        for idx, line in enumerate(self.decisionCode):
            if re.search("^\s*package\s+.+\s*\/\s*inline;", line):
                rootPackageIdx= idx

        #get the start of execute() method in the last package
        executeIdx= rootPackageIdx
        for line in self.decisionCode[rootPackageIdx:]:
            if re.search("^\s*method\s+execute\s*\(", line):
                break
            executeIdx+= 1

        #get the execute() method with all parameters
        executeMethod= ''
        for line in self.decisionCode[executeIdx:]:
            executeMethod+= line
            if re.search("^\s*.*\s*\)\s*;", line):
                break
                
        #extract parameters from root execute() method
        decisionParameters= re.sub("^\s*method\s+execute\s*\(\s*", '', executeMethod)
        decisionParameters= re.sub("\s*\)\s*;", '', decisionParameters)
        self.parameterList= decisionParameters.split(',')

        #remove white space
        for idx, parameter in enumerate(self.parameterList):
            self.parameterList[idx]= parameter.strip()
            
        return

    ################################################################################
    #prepare the parameters to generate the code for the decision flow
    ################################################################################
    def prepareParameters(self):
        outputPara= []
        for idx in range(0,len(self.parameterList)):
            #remove underscore from input parameter name
            if self.parameterList[idx][len(self.parameterList[idx])-2] == '_':
                self.parameterList[idx]= self.parameterList[idx][0:len(self.parameterList[idx])-2] + '"'
            
            #copy output parameters for further processing
            if self.parameterList[idx].find('in_out ') >= 0:   
                self.parameterList[idx]= self.parameterList[idx].replace('in_out ', '')   
                #copy paremeter and type
                outputPara.append(self.parameterList[idx])
                #we just need the parameter name - remove the rest
                self.outputParaKeep+= re.sub('^\s*\w+\s*\w*\s*"', '"', self.parameterList[idx])  +' '
                
        self.outputParaKeep+= ';'  
        
        #prepare the parameter for declaring in the calling method
        for parameter in outputPara:
            if parameter.find('package ') >= 0:
                buffer= parameter.replace('package', '')
                buffer= buffer.replace('datagrid', 'varchar(10485760)')
                self.outputParaDcl.append('dcl ' + buffer +';')
                buffer= parameter[0:len(parameter)-1] + '_dg"()'
                self.outputParaDcl.append('dcl ' + buffer +';')
            elif parameter.find('varchar ') >= 0:
                buffer= parameter.replace('varchar', 'varchar(1000)')
                self.outputParaDcl.append('dcl ' + buffer +';')
            else:
                self.outputParaDcl.append('dcl ' + parameter +';')

        #rename the datagrid variables with suffix _dg
        for idx, parameter in enumerate(self.parameterList):
            self.parameterList[idx]= self.parameterList[idx][self.parameterList[idx].find('"'):]
            if parameter.find('package ') >= 0:
                self.parameterList[idx]= self.parameterList[idx][0:len(self.parameterList[idx])-1] + '_dg"'
                self.outDataGridList.append(self.parameterList[idx])

        return        

    ################################################################################
    #Output decision code that can run in SPRE
    ################################################################################
    def writeDecisionCode(self):

        callExecute=  'dcf.execute('
        callExecute+= ",".join(self.parameterList)
        callExecute+= ');'

        codeFileName= self.codeDir + '/' +self.artefactID +'.ds2'
        
        #we check f the file already exists. In case we create it first time we set access to 777 at the end of this function
        bFileNew= False
        if os.path.isfile(codeFileName):
            bFileNew= True
            
        try:
            fCode= open(codeFileName, 'w')
        except:
            self.log("Could not open code file " + codeFileName)
            sys.exit()
    
        #write decision code ds2 package generated by ID
        for line in self.decisionCode:
            fCode.write(line + '\n')
        
        #write ds2 data step to call decision flow package
        fCode.write('data ' +self.output_table +' (overwrite=yes);\n')
        fCode.write('    ' +self.outputParaKeep +'\n')
        fCode.write('    dcl package ' +self.decision_name +' dcf();\n')
        for parameter in self.outputParaDcl:
            fCode.write('    ' +parameter +'\n')
        fCode.write('    method run();\n')
        fCode.write('        set ' +self.input_table +';\n')
        fCode.write('        ' +callExecute +'\n')
        for dg in self.outDataGridList:
            fCode.write('        ' +dg[0:len(dg)-4] +'"= ' +dg +'.serialize();\n')
        for dg in self.outDataGridList:
            fCode.write('        ' +dg +'.clear();\n')
        fCode.write('        end;\n    run;\nquit;\n')
        fCode.close()     

        #we want this file to be accessed by anyone
        if bFileNew is False:
            os.chmod(codeFileName, 0o777) 

        return codeFileName
        

