registerClient version 1.0

Program to register a client in SAS Viya in order to authorize when using SAS Viya REST APIs.

Assumption: The program is executed on the same server where SAS Viya (MAS) is installed and Python 3.x is installed. 

To execute program, copy python program to your Linux home directory and call:
	python registerClient <ClientId> <Secret>
Example:
	python registerClient mas.client Orion123

You can also call the program without any parameters to register a default ClientId 'mas.client' with secret 'Orion123'
