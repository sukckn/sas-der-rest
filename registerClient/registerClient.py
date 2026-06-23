##############################################################################
# registerClient
# Program to register a client in SAS Viya in order to authorize when calling SAS REST APIs.
# Call: python registerClient.py <ClientId> <Secret>
# You can also call the program without any parameter to register the default ClientId mas.client with secret Orion123
##############################################################################
import requests
import os
import json
import sys

# get input parameters
runOnDefault= False
if len(sys.argv) == 1:
	q= input("Do you want register the default ClientId <mas.client> with Secret <Orion123> (y/n)?")
	if q == "y":
		runOnDefault= True
	else:
		print("No ClientId registered!")
		sys.exit()
elif len(sys.argv) != 3:
	print("Not enough parameters.")
	print("registerClient <Client Id> <Secret>")
	sys.exit()

if runOnDefault:
	server= '127.0.0.1'         # Server hosting Viya. As we need to execute the programe on the Viya server we can hard coe the IP address
	clientId= 'mas.client'      # Client Id for authentication. For the KYC server this is set to "kyc"
	clientSecret= 'Orion123'    # Password for the Client Id
else:
	server= '127.0.0.1'         # Server hosting Viya. As we need to execute the programe on the Viya server we can hard coe the IP address
	clientId= sys.argv[1]       # Client Id for authentication. For the KYC server this is set to "kyc"
	clientSecret= sys.argv[2]   # Password for the Client Id

#because of reading the consul token we have to execute the program on the Viya server.
#get consult token. Assuming sas Viya got installed in the default location. 
cmdResult= os.popen("cat /opt/sas/viya/config/etc/SASSecurityCertificateFramework/tokens/consul/default/client.token", "r", 1)
consulToken= cmdResult.read()

# prepare URL - setting the server
url= "http://%s/SASLogon/oauth/clients/consul?callback=false&serviceId=%s" % (server, clientId)
# preparing the URL header
headers = {"X-Consul-Token":consulToken}
# calling the URL as POST request
try:
    response = requests.post(url, headers=headers)
except:
    print("Could not connect to server.")
    print("Check if server ip address is correct.")
    sys.exit()

# check if URL call was successful
if response.status_code < 200 or response.status_code >= 300:
    print(response)
    try:
        print(response.json()['error'])
        print(response.json()['error_description'])
    except:
        print('URL: ', url) 
        print('Consul-Token: ', consulToken)
        sys.exit()
    print('Error receiving access token!')
    sys.exit()

# grap the user token from the URL response. The token is used when calling the next URL 
token= response.json()['access_token']

# prepare URL - setting the server
url= "http://%s/SASLogon/oauth/clients" % (server)
# preparing the URL header
headers = {"Content-Type":"application/json", "Authorization": ""}
headers["Authorization"]= "Bearer " + token

#we can generate a client 'sas.sasall' id to work with all endpoints
if clientId == 'sas.sasall':
	scope= ["uaa.admin","uaa.resource","clients.read","clients.write","clients.secret","scim.read","scim.write","clients.admin","openid","*"]
else:
	scope= ["openid","*"]
	
body= {
    "client_id": clientId,
    "client_secret": clientSecret,
    "scope": scope,
    "authorized_grant_types": ["password"],
    "access_token_validity": 43200
  }
#convert dictionary to json
bodyJSON= json.dumps(body)
# calling the URL as POST request
response = requests.post(url, headers=headers, data=bodyJSON)

# check if URL call was successful
if response.status_code < 200 or response.status_code >= 300:
    print(response)
    try:
        print(response.json()['error'])
        print(response.json()['error_description'])
    except:
        print('URL: ', url) 
        sys.exit()
    print('Could not register client!')
    sys.exit()

# output success
print("Client Id: '" +  clientId + "' with Secret: '" + clientSecret + "' successfully registered.")

##### -End of Program- #####
