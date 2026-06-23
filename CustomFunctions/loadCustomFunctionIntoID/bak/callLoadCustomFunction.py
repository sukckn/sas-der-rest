import sys
sys.path.insert(0, "/home/sas/dmn")
import loadCustomFunction as lcf

def loadCustomFunction(code, description, categoryName, token=''):
    "Output: message"
    
    loadFunc= lcf.loadCustomFunction(logFileName="loadCustomFunction.log", logDir="/tmp")
    loadFunc.setStdout()
    loadFunc.setLogLevel(4)
    loadFunc.setViyaConnectInfo(server= "10.96.14.17", token=token)
    #loadFunc.setViyaConnectInfo(server= "10.96.14.17", uid="sasdemo", pwd="Orion123", clientId="sas.ec", clientSecret="")
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

if __name__ == '__main__':
    code= "method QQQ();end;"
    description= "test test test"
    categoryName= "ASD"
    token= "eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vbG9jYWxob3N0L1NBU0xvZ29uL3Rva2VuX2tleXMiLCJraWQiOiJsZWdhY3ktdG9rZW4ta2V5IiwidHlwIjoiSldUIn0.eyJqdGkiOiJmMGYxNjA5MjAxM2I0YTI1ODk3YWQ5OWU0ZDlmZGNlNiIsImV4dF9pZCI6InVpZD1zYXNkZW1vLG91PXVzZXJzLGRjPXZpeWFkZW1vLGRjPWNvbSIsInN1YiI6ImNiMTE3NWI4LWIwZGYtNDgyMS1iMGZjLTk3MTQyODE1NzIyYSIsInNjb3BlIjpbImNsaWVudHMucmVhZCIsInN2aXVzcnMiLCJjbGllbnRzLnNlY3JldCIsInVhYS5yZXNvdXJjZSIsIm9wZW5pZCIsInVhYS5hZG1pbiIsImNsaWVudHMuYWRtaW4iLCJzY2ltLnJlYWQiLCJzdmlhZG1zIiwiU0FTQWRtaW5pc3RyYXRvcnMiLCJjbGllbnRzLndyaXRlIiwic2NpbS53cml0ZSIsIkNBU0hvc3RBY2NvdW50UmVxdWlyZWQiXSwiY2xpZW50X2lkIjoic2FzLmVjIiwiY2lkIjoic2FzLmVjIiwiYXpwIjoic2FzLmVjIiwiZ3JhbnRfdHlwZSI6InBhc3N3b3JkIiwidXNlcl9pZCI6ImNiMTE3NWI4LWIwZGYtNDgyMS1iMGZjLTk3MTQyODE1NzIyYSIsIm9yaWdpbiI6ImxkYXAiLCJ1c2VyX25hbWUiOiJzYXNkZW1vIiwiZW1haWwiOiJzYXNkZW1vQG5vbmUuc2FzLmNvbSIsImF1dGhfdGltZSI6MTYwNjgyOTEyMywicmV2X3NpZyI6IjI5NDIyM2RjIiwiaWF0IjoxNjA2ODI5MTIzLCJleHAiOjE2MDY4NjUxMjMsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3QvU0FTTG9nb24vb2F1dGgvdG9rZW4iLCJ6aWQiOiJ1YWEiLCJhdWQiOlsic2NpbSIsImNsaWVudHMiLCJzYXMuKiIsInVhYSIsIm9wZW5pZCIsInNhcy5lYyJdfQ.f5HRNzdEu4VU22jU7AAAIsHnMm81fEvFwhOd4PnQpk-FTMizmYzfcPzZ1OSpJeBEF3Asfs7zx58eSH-BXC2PfvwRYFaSLM9JDoffKNdm-bAL4D54rTO9Cn5wDOvK32cgzTpS77ofELAptvLUTxdJysodBYlgw9Gwc-HjzVk1ukro2V9EPY7Tc_0qYmLjWsixQlr1a-1iTDZF3Z1dY3LMMaCi-TOl0lGyMvi3UI6LyoRCRCcxQT1RAMakaWzf-tX97WvKeQRUG1NyjS7thWDhecQYDhUhoBc-bnvgTS1jmU3LGEY6H6agXrRKlzYAEihv_ruvhS4ykiM0rR6xyuhdog"
    msg= loadCustomFunction(code, description, categoryName, token)
    print(msg)
    
