# Coding: utf-8
# Description: Convert CSV export of CloudGuard policies into JSON policy files grouped by tactic and severity
# Author: Sven Bracke <sven.bracke@orangecyberdefense.com>
# Date: 2022-12-20

import json
import csv

# Global vars def
# Platform: azu, aws or gcp

platform = "azu"
policy_version = 'v1.1.1'
csvFilePath = f'csv_export/ocd_{platform}_{policy_version}.csv'

#def make_json(csvFilePath, jsonFilePath):
# create a dictionary

tactics = {}

# Open a csv reader called DictReader
# We use the setdefault method to automatically create a dictionary and a list according to the category and severity
# Make sure the CSV file has a severity and category in each row and, no empty rows exist or it will generate an error that the "file was not found"

import chardet
with open(csvFilePath, 'rb') as rawdata:
    result = chardet.detect(rawdata.read(100000))
result

with open(csvFilePath, encoding=result['encoding']) as csvf:
    csvReader = csv.DictReader(csvf, delimiter=';')
    for row in csvReader:
        row.pop("id")
        tactics.setdefault(row["Category"],{}).setdefault(row['Severity'],[]).append(row)

# We write JSON file per tactic and per severity make sure there is no trailing whitespace in the severity or tactic or the file will not be found

for tactic, value in tactics.items():
    for severity, rules in value.items():
        tactic = str(tactic).replace(" ", "-").lower()
        if platform == "azu":
            with open(f'policy/ocd/azure/{tactic}/azure-{severity.lower().strip()}-{tactic}-{policy_version}.json', 'r', encoding=result['encoding']) as handle:
                json_data = handle.read()
                json_dict = json.loads(json_data)
                json_dict['rules'] = rules
                json_dict['name'] = f"OCD: {platform.upper()} {tactic} ({severity.upper()}) {policy_version}"
            with open(f'policy/ocd/azure/{tactic}/azure-{severity.lower().strip()}-{tactic}-{policy_version}.json', 'w', encoding=result['encoding']) as handle:
                handle.write(json.dumps(json_dict, indent=4))
        elif platform == "aws":
            with open(f'policy/ocd/aws/{tactic}/aws-{severity.lower().strip()}-{tactic}-{policy_version}.json', 'r', encoding=result['encoding']) as handle:
                json_data = handle.read()
                json_dict = json.loads(json_data)
                json_dict['rules'] = rules
                json_dict['name'] = f"OCD: {platform.upper()} {tactic} ({severity.upper()}) {policy_version}"
            with open(f'policy/ocd/aws/{tactic}/aws-{severity.lower().strip()}-{tactic}-{policy_version}.json', 'w', encoding=result['encoding']) as handle:
                handle.write(json.dumps(json_dict, indent=4))
        elif platform == "gcp":
            with open(f'policy/ocd/gcp/{tactic}/gcp-{severity.lower().strip()}-{tactic}-{policy_version}.json', 'r', encoding=result['encoding']) as handle:
                json_data = handle.read()
                json_dict = json.loads(json_data)
                json_dict['rules'] = rules
                json_dict['name'] = f"OCD: {platform.upper()} {tactic} ({severity.upper()}) {policy_version}"
            with open(f'policy/ocd/gcp/{tactic}/gcp-{severity.lower().strip()}-{tactic}-{policy_version}.json', 'w', encoding=result['encoding']) as handle:
                handle.write(json.dumps(json_dict, indent=4))