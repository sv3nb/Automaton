#!/usr/bin/env python
# coding: utf-8

#Description: construct network-mapped data based on ATT&CK matrix filtered on Threat Group. Data Can be used for building risk profiles and Security Assessment reports
#Author: Sven Bracke
#Date: 2022-09-06 
#Version: 1.1

# construct a dataframe bases on ATT&CK matrix filtered on Threat Group. 
# Data can be used for building risk profiles in Algosec and copy pasted into Security Assessment reports

from base64 import encode
from typing import Collection
import pandas as pd
import requests, bs4
from lxml import etree


df = pd.read_json('FIN6_(G0037).json')
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_colwidth', None)


# construct a hyperlink for all matching techniques we will use this to webscrape the mitigations

def concat(technique):
    technique = technique.replace('.', '/')
    return f"https://attack.mitre.org/techniques/{technique}"

df['Link']  = df['techniqueID'].apply(concat)

# Construct a Traffic column based on the tactic

def traffic_matcher(tactic):
    if tactic == "initial-access":
        return ["From EXTERNAL To DMZ"]
    elif tactic == "collection":
        return ["From INTERNAL To INTERNAL"]
    elif tactic == "lateral-movement":
        return ["From DMZ To INTERNAL", "From INTERNAL To DMZ", "From INTERNAL To INTERNAL"]
    elif tactic == "discovery":
       return ["From INTERNAL To INTERNAL", "From DMZ To INTERNAL"]
    elif tactic == "exfiltration":
        return ["From DMZ To EXTERNAL"]
    elif tactic == "command-and-control":
        return ["From DMZ To EXTERNAL", "From INTERNAL To EXTERNAL"]

df['Traffic'] = df['tactic'].apply(traffic_matcher)

# Webscraper to extract Mitigations
# Use XPATH to extract deep nested data
# The second table of the selected class contains the <p> elements that describe the mitigations hence we select root[1] and search for <p> child elements

def scrape_mitigation(url):
    res = requests.get(url)
    res.raise_for_status()
    technique = bs4.BeautifulSoup(res.text, 'html.parser')
    dom = etree.HTML(str(technique))
    root = technique.findAll('table', {'class': 'table table-bordered table-alternate mt-2'})
    try:
        children = root[1].findChildren('p', recursive=True)
    except IndexError:
        number = 0
    else:
        number = len(children)
    mitigation_list = []

    # for certain (sub)techniques there is no mitigation
    if number == 0:
        return "This type of attack technique cannot be easily mitigated"
    elif number <= 1:
        mitigation_list.append(dom.xpath('//*[@id="v-attckmatrix"]/div[2]/div/div/div/table[2]/tbody/tr[1]/td[3]/p/text()')[0])
    else:
        for i in range(1,number + 1): # added + 1 or else he misses the last mitigation.
            try:
                mitigation_list.append(dom.xpath(f'//*[@id="v-attckmatrix"]/div[2]/div/div/div/table[2]/tbody/tr[{i}]/td[3]/p/text()')[0])
            except IndexError:
                continue
    return mitigation_list

df['Mitigations'] = df['Link'].apply(scrape_mitigation)
df["Mitigations"].str.wrap(5)

# Webscraper to extract Description

def scrape_description(url):
    res = requests.get(url)
    res.raise_for_status()
    technique = bs4.BeautifulSoup(res.text, 'html.parser')
    desc = technique.select('div.description-body')
    mylist = [(p.get_text(strip=True)) for p in desc]
    return mylist[0]

df['Description'] = df['Link'].apply(scrape_description)

# We can construct a list of protocols found within the comment column and use it to construct the "Services" column.
# Might better use the Description of the technique since it contains more info

def service_matcher(desc):
    network_protocols = [ \
        'FTP', 'VPN', 'enumeration', 'SMB', 'RDP', 'RPC',\
        'Windows remote', 'Kerberos', 'WMI', 'SQL', 'HTTP', 'HTTPS', 'LDAP',\
        'SSH', 'TELNET', 'SSL', 'TLS' \
        ]
    protocol_list = []
    for protocol in network_protocols:
        if protocol.lower() in desc.lower():
            protocol_list.append(protocol)
    return protocol_list

df['Services'] = df['Description'].apply(service_matcher)


# Final prep of filtered dataframe
tactics = ['initial-access', 'lateral-movement', 'exfiltration', 'collection', 'command-and-control']

# and use them as a filter
filt = (df['tactic'].isin(tactics))
final = (df.loc[filt, ['tactic', 'Services', 'Traffic', 'Mitigations', 'Link']]) # create a new filtered dataframe with just these columns
final
final.to_excel('FIN6_Map.xlsx', engine='openpyxl')
final.to_json('FIN6_Map.json', indent= 4)