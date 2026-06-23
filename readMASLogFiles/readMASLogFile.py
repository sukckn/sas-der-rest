import requests
import base64
import json
import pandas as pd
import collections as co
import sys

# get input parameters
if len(sys.argv) != 5:
	print("Not enough parameters.")
	print("readMasLogFile <server address> <userid> <passowrd>")
	sys.exit()

# Logon Credentials. 
server= sys.argv[1]
uid= sys.argv[2]
pwd= sys.argv[3]
clientId= 'sas.ec'
clientSecret= ''
#Set 'Y' to only get the log information for today. 'N' to get the hwole log file.
todayOnly= sys.argv[4]

# MAS Parameters
MasService= 'maslogfiles'
# Create input parameter variables here and assign input value
#<InputParameter_1>= <InputValue>

# Determine which fields to output from MAS Service and in which order
# In outFlields list name field in order you want to output
outFlields= ["logFileContent"]

# Set JSON input structure here. 
inputData={
    "inputs": [
    {
    "name": "logfilename",
    "value": "1"
    },
    {
    "name": "todayonly",
    "value": "Y"
    }]}

# Assign input data here. Duplicate line below and adjust settings as necessary.
#inputData["inputs"][0]["value"]= <input parameter variable>

# Make Python dictionary into JSON object
inputDataJSON= json.dumps(inputData)

loginCredentials={"grant_type":"password","username":uid,"password":pwd}
appBinding= clientId + ':' + clientSecret
appBinding64= base64.b64encode(bytes(appBinding, 'utf-8'))
url= "http://%s/SASLogon/oauth/token" % (server)

headers = {"Content-Type":"application/x-www-form-urlencoded", "Authorization":"Basic "}
headers["Authorization"]= "Basic " + appBinding64.decode('ascii') #appBinding64 is type bytes but need to convert to type str
response = requests.post(url, headers=headers, data=loginCredentials)

if response.status_code < 200 or response.status_code >= 300:
    print('Error receiving user token!')
    print(pd.DataFrame([response.json()]))
    quit()
else:
    token= response.json()['access_token']


# ### Call MAS Service
url= "http://%s//microanalyticScore/modules/%s/steps/readmaslogfile" % (server, MasService)

headers = {"Content-Type":"application/json", "Authorization":"Bearer "}
headers["Authorization"]= "Bearer " + token
response = requests.post(url, headers=headers, data=inputDataJSON)

if response.status_code < 200 or response.status_code >= 300:
    print('Error calling MAS service!')
    print(response.json()['message'])
    pd.options.display.max_colwidth = -1
    print(pd.DataFrame(data= response.json()['details']))
    quit()


# ### Output return data
file= open('maslog.log','w') 
for line in json.loads(response.json()['outputs'][0]['value']):
    file.write(line)
file.close()
