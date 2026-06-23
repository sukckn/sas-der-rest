import requests
import base64
import json
import sys 
import re
sys.path.insert(0, "/etc/sas/pycode")
import saslog

class loadCustomFunction:
    custFuncId= ''
    funcName= ''
    
########################################################################################################
    def __init__(self, server="127.0.0.1", token=None, uid="", pwd="", clientId="", clientSecret="", logFileName="", logDir=""):
        #initilise the log file
        self.log= saslog.saslog(logLevel=0, logFileName=logFileName, logDir=logDir)
        #set viya connection information 
        self.setViyaConnectInfo(server, token, uid, pwd, clientId, clientSecret)
        
########################################################################################################
    def setViyaConnectInfo(self, server="127.0.0.1", token=None, uid="", pwd="", clientId="", clientSecret=""):
        self.log.out("setViyaConnectInfo():", 2)
        #set Viya logon information
        self.server= server
        if token != None:
            self.token= token
        if uid != "":
            self.uid= uid
        if pwd != "":
            self.pwd= pwd
        if clientId != "":
            self.clientId= clientId
        if clientSecret != "":
            self.clientSecret= clientSecret
        
        #if there is no token and user credentials are supplied we ask for a user token.
        if len(uid) > 0 and len(clientId) > 0 and token == None:
            self.getToken()
        self.log.out("Token: " +str(self.token), 4)
        return

########################################################################################################
    def setStdout(self, switch=True):
        #it true log info will also output to the screen
        self.log.setStdout(switch)
        return

########################################################################################################
    def setLogLevel(self, logLevel):
        #set loglevel. The higher the more information will be written out 
        self.log.setLogLevel(logLevel)
        self.log.out("LogLevel= " +str(logLevel), 2)
        return

########################################################################################################
    def getToken(self, forceToken=False):
        self.log.out("getToken():", 2)
        #if a token is set already we don't ask for a new one unless we force (forceToken=True) to get a token
        if self.token != None and forceToken == False:
            self.log.out("token: " + self.token, 3)
            return
            
        loginCredentials={"grant_type":"password","username":self.uid,"password":self.pwd}
        appBinding= self.clientId + ':' + self.clientSecret
        appBinding64= base64.b64encode(bytes(appBinding, 'utf-8'))
        url= "http://%s/SASLogon/oauth/token" % (self.server)

        headers = {"Content-Type":"application/x-www-form-urlencoded", "Authorization":"Basic "}
        headers["Authorization"]= "Basic " + appBinding64.decode('ascii') #appBinding64 is type bytes but need to convert to type str
        try:
            response = requests.post(url, headers=headers, data=loginCredentials)
        except Exception as err:
            self.log.out(err)
            self.exitProg()
        
        if response.status_code < 200 or response.status_code >= 300:
            self.log.out('Error receiving user token!')
            self.log.out(response.json())
            self.log.out("user:         >" + self.uid + "<", 4)
            self.log.out("password:     >" + self.pwd + "<", 4)
            self.log.out("clientId:     >" + self.clientId + "<", 4)
            self.log.out("clientSecret: >" + self.clientSecret + "<", 4)
            self.exitProg()
        
        self.token= response.json()['access_token']
        self.log.out("token: " + self.token, 3)
        #print("token: " + self.token)

        return
        
########################################################################################################
    def getCategories(self, catName):
        self.log.out("getCategories():", 2)
        url= 'http://%s/businessRules/functionCategories?filter=eq(name,"%s")' % (self.server, catName)

        headers = {"Content-Type":"application/json", "Authorization":"Bearer "}
        headers["Authorization"]= "Bearer " + self.token
        try:
            response = requests.get(url, headers=headers)
        except Exception as err:
            self.log.out(err)
            self.exitProg()

        self.log.out("getCategories():", 2)
        self.log.out("    url: " + url, 3)

        if response.status_code < 200 or response.status_code >= 300:
            self.log.out('Error receiving categories!')
            self.log.out(response.json())
            self.exitProg()
            
        self.category= ''
        if response.json()['count'] > 0:
            self.category= response.json()['items'][0]['name']
            self.categoryId= response.json()['items'][0]['id']
            
            self.log.out("    category: " +self.category, 2)
            self.log.out("    categoryId: " + self.categoryId, 2)
        else:
            self.log.out("    category does not exist. Need to create it.", 2)

        return self.category
        
########################################################################################################
    def createCategory(self, catName):
        self.log.out("createCategory():", 2)

        #if the category alraedy exists we don't create it
        if len(self.getCategories(catName)) > 0:
            self.log.out("    category '" +catName +"' already exist.", 3)
            return
    
        url= 'http://%s/businessRules/functionCategories/' % (self.server)

        cat= {"name": catName}
        payload= json.dumps(cat)
        self.log.out("    paload:" +str(payload), 3)
        
        headers = {"Content-Type":"application/json", "Authorization":"Bearer "}
        headers["Authorization"]= "Bearer " + self.token
        try:
            response = requests.post(url, headers=headers, data=payload)
        except Exception as err:
            self.log.out(err)
            self.exitProg()

        self.log.out("    url: " + url, 3)

        if response.status_code < 200 or response.status_code >= 300:
            self.log.out('Error creating category!')
            self.log.out(response.json())
            self.exitProg()         

        self.categoryId= response.json()['id']
        self.log.out("    categoryId: " + self.categoryId, 2)

        return
    
########################################################################################################
    def getFunctionInfo(self, code='', funcName=''):
        self.log.out("getFunctionInfo():", 2)
        #if the ds2 code was passed in we takse the function name from the source code
        if len(code) > 0:
            funcName= self.getFunctionName(code)
        self.funcName= funcName
        
        #check in function exists
        url= 'http://%s/businessRules/functions?filter=eq(name,"%s")' % (self.server, funcName.lower())        

        headers = {"Content-Type":"application/json", "Authorization":"Bearer "}
        headers["Authorization"]= "Bearer " + self.token
        try:
            response = requests.get(url, headers=headers)
        except Exception as err:
            self.log.out(err)
            self.exitProg()

        self.log.out("    url: " + url, 3)

        if response.status_code < 200 or response.status_code >= 300:
            self.log.out('Error function information (Name)!')
            self.log.out(response.json())
            self.exitProg()

        if response.json()['count'] > 0:
            self.custFuncId= response.json()['items'][0]['id']
            self.log.out("    functionId: " + self.custFuncId, 2)
            self.log.out("    categoryId: " + self.categoryId, 2)
            if response.json()['items'][0]['categoryId'] != self.categoryId:
                self.log.out("    categoryId has changed. Function will be moved into new category folder!", 2)            
        else:
            self.log.out("    Function '" + funcName +"' does not exist. Need to create it.", 2)                    
            return
        
        #get E-Tag it is needed for the update call
        url= 'http://%s/businessRules/functions/%s' % (self.server, self.custFuncId)        

        headers = {"Content-Type":"application/json", "Authorization":"Bearer "}
        headers["Authorization"]= "Bearer " + self.token
        try:
            response = requests.get(url, headers=headers)
        except Exception as err:
            self.log.out(err)
            self.exitProg()

        self.log.out("    url: " + url, 3)

        if response.status_code < 200 or response.status_code >= 300:
            self.log.out('Error function information (ID)!')
            self.log.out(response.json())
            self.exitProg()
        
        self.ifMatch= response.headers['ETag']
        self.log.out("    E-Tag: " + self.ifMatch, 2)     
        return


########################################################################################################
    def createFunction(self, code, description=''):
        self.log.out("createFunction():", 2)
        url= 'http://%s/businessRules/functionCategories/%s/functions' % (self.server, self.categoryId)

        funcInfo= {}
        funcInfo['description']= description
        funcInfo['code']= code
        payload= json.dumps(funcInfo)
        self.log.out("    paload:" +str(payload), 3)


        headers = {"Content-Type":"application/json", "Authorization":"Bearer "}
        headers["Authorization"]= "Bearer " + self.token
        
        try:
            response = requests.post(url, headers=headers, data=payload)
        except Exception as err:
            self.log.out(err)
            self.exitProg()

        self.log.out("    url: " + url, 3)

        if response.status_code < 200 or response.status_code >= 300:
            self.log.out('Error creating function!')
            self.log.out(response.json())
            self.exitProg()         

        self.categoryId= response.json()['id']
        self.log.out("Created function: " +self.funcName, 0)
        return self.categoryId
        
########################################################################################################
    def updateFunction(self, code, description=''):
        self.log.out("updateFunction():", 2)
        url= 'http://%s/businessRules/functions/%s' % (self.server, self.custFuncId)

        funcInfo= {}
        funcInfo['categoryId']= self.categoryId
        funcInfo['description']= description
        funcInfo['code']= code
        payload= json.dumps(funcInfo)
        self.log.out("    paload:" +str(payload), 3)

        headers = {"Content-Type":"application/json", "Authorization":"Bearer "}
        headers["Authorization"]= "Bearer " + self.token
        headers["If-Match"]= self.ifMatch
        
        try:
            response = requests.put(url, headers=headers, data=payload)
        except Exception as err:
            self.log.out(err)
            self.exitProg()

        self.log.out("    url: " + url, 3)

        if response.status_code < 200 or response.status_code >= 300:
            self.log.out('Error updating function!')
            self.log.out(response.json())
            self.exitProg()         

        self.categoryId= response.json()['id']
        self.log.out("Updated function: " +self.funcName, 0)
        return self.categoryId
        
########################################################################################################
    def getFunctionName(self, code):
        self.log.out("getFunctionName():", 2)
        #extract the method name from the ds2 code.
        regex = r"^( *method *)([a-z0-9_]*)(\()(.*)"
        matches = re.finditer(regex, code, re.MULTILINE | re.IGNORECASE)
        methodName= ''
        for matchNum, match in enumerate(matches, start=1):
            methodName= match.group(2)
        self.log.out("FunctionName: " +methodName, 2)
        return methodName
        
########################################################################################################
    def exitProg(self):
        print("Error creating/updating custom function. Check log file " + self.log.getLogName())
        sys.exit()
        
        