#! /usr/bin/env pythonpyt   

# Download the threat group matrix and save it to a JSON file so we can load it into a jupyter notebook
# adds some additional info 

import requests, bs4
import json

### USER INPUT ###

Threat_Group = "G0047"
Layer = "enterprise" # enterprise, mobile or ics

### END USER INPUT ###

Url = f"https://attack.mitre.org/groups/{Threat_Group}/{Threat_Group}-{Layer}-layer.json"

resp = requests.get(Url)
matrix = json.loads(resp.text)

for technique in matrix['techniques']:
    techniqueID = str(technique['techniqueID']).replace('.', '/')
    technique['link'] = f'https://attack.mitre.org/techniques/{techniqueID}'
    res = requests.get(technique['link']) 
    content = bs4.BeautifulSoup(res.text, 'html.parser')


with open(f"{Threat_Group}.json", "w") as jsonfile:
    json.dump(matrix['techniques'], jsonfile, indent=4, sort_keys=True)

