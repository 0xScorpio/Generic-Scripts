import requests
import urllib3
import pandas as pd
from pandas import json_normalize
import json
import pprint
import os
import time

# disabled SSL warnings for local install
urllib3.disable_warnings()

output = {

    "format": "csv",
    "reportContents": {
        "csvColumns": {
            "id": False,
            "cve": True,
            "cvss": False,
            "risk": True,
            "hostname": True,
            "protocol": True,
            "port": True,
            "plugin_name": True,
            "synopsis": False,
            "description": True,
            "solution": True,
            "see_also": False,
            "plugin_output": True,
            "stig_severity": False,
            "cvss3_base_score": False,
            "cvss_temporal_score": False,
            "cvss3_temporal_score": False,
            "risk_factor": False,
            "references": False,
            "plugin_information": False,
            "exploitable_with": False
        }
    },
    "extraFilters": {
        "host_ids": [],
        "plugin_ids": []
    }
}

# connection/authentication strings
nessus_api_url = "https://localhost:8834"
accessKey = input('Enter Nessus API access key:\n')
secretKey = input('Enter Nessus API secret key:\n')

headers = {
	'Content-type': 'application/json',
	'X-ApiKeys': f'accessKey={accessKey}; secretKey={secretKey}'
}

sleepPeriod = 5

# initialize a session without needing to authenticate repeatedly
session = requests.session()
session.headers.update(headers)

# connect/authenticate
request = session.get(nessus_api_url + '/scans', verify=False)

# status code debug
print(request.status_code)

# print return data from request
pprint.pprint(request.json())


################## JSON NORMALIZATION #####################
folders = json.loads(request.text)['folders']
scans = json.loads(request.text)['scans']

folders_df = json_normalize(folders)
scans_df = json_normalize(scans)

list_of_folders = folders_df.id.to_list()
scans_dictionary = pd.Series(scans_df.name.values, index=scans_df.id).to_dict()

for item in list_of_folders:
	print(item)

for scan_id, name in scans_dictionary.items():
	print(f'{scan_id}:{name}')


########################## DATA STORAGE ##########################
data_storage = 'Nessus_Exports'

if not os.path.exists(data_storage):
	print('Folder does not exist! Creating...')
	os.makedirs(data_storage)
else:
	print('Folder exists!')


######################## EXPORT! ###############################
for scan_id, name in scans_dictionary.items():
	# variables
	scan_url = f'{nessus_api_url}/scans/{scan_id}/export'
	scan_request = session.get(url=scan_url, verify=False)
	jsonOutput = json.dumps(output)

	# post request
	r = requests.post(url=scan_url, headers=headers, data=jsonOutput, verify=False)

	# status variables
	jsonData = r.json()
	scanFile = str(jsonData['file'])
	scanToken = str(jsonData['token'])
	status = "loading"

	# check ready status
	while status != 'ready':
		
		URL = nessus_api_url + "/scans/" + str(scan_id) + "/export/" + scanFile + "/status"
		t = requests.get(url=URL, headers=headers, verify=False)
		data = t.json()
		if data['status'] == 'ready':
			status = 'ready'
		else:
			time.sleep(sleepPeriod)

	# download report
	URL = nessus_api_url + "/scans/" + str(scan_id) + "/export/" + scanFile + "/download"
	d = requests.get(url=URL, headers=headers, verify=False)
	dataBack = d.text

	# CSV cleanup
	csvData = dataBack.split('\r\n', -1)
	NAMECLEAN = name.replace('/', '-', -1)
	print('---------------------------------------------------------')
	print("Starting Download ---> " + NAMECLEAN)
	output_file = f'{data_storage}/{NAMECLEAN}.csv'
	with open(output_file,'w',encoding='utf-8') as csvfile:
		for line in csvData:
			csvfile.writelines(line+'\n')
	print('---------------------------------------------------------')
	print("Export completed for " + NAMECLEAN + "!")
contents here
