The Python script requires Python 3.x
Currently the script is pointing to an Anaconda Python installation on Linux. 
	#!/opt/sasinside/anaconda3/bin/python3
	You need to adjust this as appropriate.

Installaion:
	Copy the file into a directory on Linux
	Make file execuatble: chmod 555 transfer_get_export_uris.py
	Execute:
		usage: transfer_get_export_uris [-h] --uri URI [--file FILE] [--dir DIR]

		Generates JSON file for 'sas-admin transfer export' to transfer decision with all objects.

		optional arguments:
		  -h, --help            show this help message and exit
		  --uri URI, -u URI     Specifies the relative URI of the decision to be exported.
		  --file FILE, -f FILE  Specifies the JSON filename to create with decision URIs to export. Default file name is <decision name>_uris.json
		  --dir DIR, -d DIR     Specifies directory where the json file is generated. Default is the user home directory.
