#!/opt/sasinside/anaconda3/bin/python3
# -*- coding: utf-8 -*-
#
#transfer_get_export_uris.py
#October 2020
#
#transfer_get_export_uris is an addition to the CLI transfer plugin. It is doing a deep scan of a decision flow and 
#generates a json file with all necessary URIs to to export a decision flow from SAS Intelligent Decisioning.
#Pass in a decision URI to get the URIs for all invoked Objects like RuleSets, Treatments, Lookup Tables, Models, etc.
#The generated file can be used as input file for 'sas-admin transfer export'
########################################################################################################

import argparse
import requests
import base64
import json
import os
from os.path import expanduser
import sys

nodeTypes= ["application/vnd.sas.decision.step.custom.object", "application/vnd.sas.decision.step.model", "application/vnd.sas.decision.step.ruleset"]
customTypes= ["treatmentGroup", "decision"]
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
    return server
    
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

#########################################################################################################
def getInfoFromID(uri, token, nodeType= ''):
    #print dot to show progress 
    print(".", end='', flush=True)
    extend= ''
    if nodeType == 'rs':
        extend= '/rules'

    url= "%s%s%s" % (server, uri, extend)
    headers = {"Content-Type":"application/json", "Authorization":"Bearer "}
    headers["Authorization"]= "Bearer " + token
    response = requests.get(url, headers=headers)

    if response.status_code < 200 or response.status_code >= 300:
        msg= response.json()['message']
        print("")
        if msg.find('Access token expired') >= 0:
            print("Access token expired! Please run: 'sas-admin auth login'")
        else:
            print("Error calling URI!")
            print(msg)
            for d in response.json()['details']:
                print(d)
        quit()
        
    return response.json()

#########################################################################################################
def getNodeUris(df_steps, nodeUris):
    uriInfo= []
    uri= ''
    nodeName= ''
    nodeType= ''
    for node in df_steps:
        if node['type'] in nodeTypes:
            if node['type'] == "application/vnd.sas.decision.step.custom.object":
                if node['customObject']['type'] in customTypes:
                    uri= node['links'][0]['uri'][0:node['links'][0]['uri'].find('/revisions')]
                else:
                    uri= node['links'][0]['uri']
                    if uri.find('/revisions') >= 0:
                        uri= uri[0:uri.find('/revisions')]
                nodeName= node['customObject']['name']
                nodeType= node['customObject']['type']

            else:
                uri= node['links'][0]['uri']
                nodeName= node[node['links'][0]['rel'].lower()]['name']
                nodeType= node['links'][0]['rel']
                                                              
            uriInfo= []
            uriInfo.append(nodeName)
            uriInfo.append(nodeType)
            nodeUris[uri]= uriInfo

        elif node['type'] == "application/vnd.sas.decision.step.condition":
            getNodeUris(node['onTrue']['steps'], nodeUris)
            getNodeUris(node['onFalse']['steps'], nodeUris)
        elif node['type'] == "application/vnd.sas.decision.step.branch":
            for branch in node['branchCases']:
                getNodeUris(branch['onTrue']['steps'], nodeUris)
            getNodeUris(node['defaultCase']['steps'], nodeUris)
    return
    
#########################################################################################################
def getLookupTableUris(rs, ltUris):
    try:
        rs['items']
    except:
        return
    
    uri= ''
    looupName= ''
    uriInfo= []
    for item in rs['items']:
        for condition in item['conditions']:
            try:
                if '/referenceData/domains/' + condition['lookup']['id'] not in ltUris:
                    uri= '/referenceData/domains/' + condition['lookup']['id']
                    looupName= condition['lookup']['name']
            except:
                pass

        for action in item['actions']:
            try:
                if '/referenceData/domains/' + action['lookup']['id'] not in ltUris:
                    uri= '/referenceData/domains/' + action['lookup']['id']
                    looupName= action['lookup']['name']
            except:
                pass
                
        if len(uri) > 0:
            uriInfo= []
            uriInfo.append(looupName)
            uriInfo.append('lookup')
            ltUris[uri]= uriInfo            
    return

#########################################################################################################
def getModelProjectUri(model, modelUris):
    uri= '/modelRepository/projects/' + model['projectId']
    projectName= model['projectName']    
    uriInfo= []
    uriInfo.append(projectName)
    uriInfo.append('modelProject')
    modelUris[uri]= uriInfo            

    return

#########################################################################################################
def getTreamentGroupMemberUris(trg, trUris):
    for member in trg['members']:
        uri= '/treatmentDefinitions/definitions/' + member['definitionId']
        treatmentName= member['definitionName']
        uriInfo= []
        uriInfo.append(treatmentName)
        uriInfo.append('treatmentDefinition')
        trUris[uri]= uriInfo            
        
        treatment= getInfoFromID(uri, token)
        getTreamentRuleSetUri(treatment, trUris)
    return 
    
#########################################################################################################
def getTreamentRuleSetUri(tr, trUris):
    try:
        uri= tr['eligibility']['ruleSetUri']
        uri= uri[0:uri.find('/revisions')]
        ruleSetName= tr['eligibility']['ruleSetName']
        
        uriInfo= []
        uriInfo.append(ruleSetName)
        uriInfo.append('ruleSet')
        trUris[uri]= uriInfo            
    except:
        pass

    return 
    
#########################################################################################################
def getDecisionUris(uri, exportUrisDic, token):
    df= getInfoFromID(uri, token)
    df_steps= df['flow']['steps']
    decisionName= df['name']

    uriInfo= []
    uriInfo.append(decisionName)
    uriInfo.append('decision')
    exportUrisDic[uri]= uriInfo            

    scanUrisDic= {}
    getNodeUris(df_steps, scanUrisDic)
    exportUrisDic.update(scanUrisDic)
          
    for nodeUri in scanUrisDic:
        if nodeUri.find('ruleSets') >= 0:
            rs= getInfoFromID(nodeUri, token, 'rs')
            getLookupTableUris(rs, exportUrisDic)
        elif nodeUri.find('models') >= 0:
            model= getInfoFromID(nodeUri, token)
            getModelProjectUri(model, exportUrisDic)
        elif nodeUri.find('definitionGroups') >= 0:
            treatmentGroup= getInfoFromID(nodeUri, token)
            getTreamentGroupMemberUris(treatmentGroup, exportUrisDic)
        elif nodeUri.find('flows') >= 0:
            decUrisDic= {}
            getDecisionUris(nodeUri, decUrisDic, token)
            exportUrisDic.update(decUrisDic)

    return decisionName

#########################################################################################################
def writeExportFile(exportUrisDic, decisionName, fileName, fileDir):
    if fileName == None:
        fileName= decisionName +'_uris.json'
    
    if fileDir == None:
        #fileDir= expanduser("~")
        fileDir= os.getcwd()
    
    fileName= os.path.join(fileDir, fileName)
    try:
        exportFile= open(fileName, "w")
    except:
        print("\nCannot write output file '" + fileName +"'")
        quit()
        
    exportFile.write('{')
    exportFile.write('"version": 1,')
    exportFile.write('"name": "' +decisionName +'",')
    exportFile.write('"description": "",')
    exportFile.write('"items": [')
    i=0
    cnt= len(exportUrisDic)
    for uri in exportUrisDic:
        if i == cnt-1:
            exportFile.write('"' +uri +'"')
        else:
            exportFile.write('"' +uri +'",')
        i+= 1
    exportFile.write(']')
    exportFile.write('}')
    exportFile.close()

    return fileName

#########################################################################################################
def outputUrisToScreen(exportUrisDic, fileName):
    print("completed")
    print("Created file '" +fileName +"' with " +str(len(exportUrisDic)) +" export URIs.")

    outputList= []
    outputRow=[]
    for uri in exportUrisDic:
        outputRow=[]
        for info in exportUrisDic[uri]:
            outputRow.append(info)
        outputRow.append(uri)
        outputList.append(outputRow)
    
    output= tuple(outputList)
    template = "{0:25}{1:25}{2:100}" # column widths: 25,25,100
    print (template.format("Object Name", "Object Type", "URI")) # header
    for row in output: 
        print(template.format(*row))    
    
    return 

#########################################################################################################
def getInputArguments():
    parser = argparse.ArgumentParser(prog="transfer_get_export_uris",
                                     description="Generates JSON file for 'sas-admin transfer export' to transfer decision with all objects.")
    parser.add_argument("--uri","-u",  help="Specifies the relative URI of the decision to be exported.",required='True')
    parser.add_argument("--file","-f", help="Specifies the JSON filename to create with decision URIs to export. Default file name is <decision name>_uris.json")
    parser.add_argument("--dir","-d", help="Specifies directory where the json file is generated. Default is current directory.")
    args = parser.parse_args()

    uri= args.uri
    fileDir= args.dir
    fileName= args.file
    
    return uri, fileDir, fileName
    
#########################################################################################################
if __name__ == '__main__':
    global server
    uri, fileDir, fileName= getInputArguments()
    print("Collecting data...", end='', flush=True)
    
    server= getServer()
    token= getAccessToken()
    exportUrisDic= {}
    decisionName= getDecisionUris(uri, exportUrisDic, token)
    fileName= writeExportFile(exportUrisDic, decisionName, fileName, fileDir)    
    outputUrisToScreen(exportUrisDic, fileName)
    
    
