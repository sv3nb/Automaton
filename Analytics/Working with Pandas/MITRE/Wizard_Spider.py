#!/usr/bin/env python
# coding: utf-8

# import a matrix filtered on Wizard_Spider group
# The schema contains metadata about the columns

import pandas as pd
schema_df  = pd.read_json('MITRE_Schema.json')
df = pd.read_json('Wizard_Spider.json')
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 50)
schema_df.set_index('column', inplace=True )
explanation = schema_df.loc['metadata', 'explanation']

print(explanation)

# filter with regex keywords

content_filter = df['comment'].str.contains('FTP|network|enumeration|SMB|RDP', na=False, case=False, regex=True) # set regex flag and we can use OR
df.loc[content_filter, ['tactic', 'techniqueID', 'comment', 'metadata']]

# different approach to return the value matched when it is found in the 'comment' series.

network_protocols = ['FTP', 'VPN', 'enumeration', 'SMB', 'RDP', 'RPC', 'Windows remote', 'RPC', 'Kerberos', 'WMI', 'SQL']
def matcher(comment):
    for protocol in network_protocols:
        if protocol.lower() in comment.lower():
            return f'network protocol used is: {protocol}'
    else:
        return 'none'

df['metadata'] = df['comment'].apply(matcher)
result = (df['metadata'] != 'none')
df.loc[result, ['tactic', 'techniqueID', 'metadata']]

# construct a hyperlink for all matching techniques

def concat(technique):
    technique = technique.replace('.', '/')
    return f"https://attack.mitre.org/techniques/{technique}"

df.loc[result, 'links']  = df.loc[result, 'techniqueID'].apply(concat)
df.loc[result, ['tactic', 'techniqueID', 'metadata', 'links']]

# create a list of keywords to search for in the column tactic

tactics = ['initial-access', 'lateral-movement', 'exfiltration', 'collection', 'command-and-control']

# and use them as a filter

filt = (df['tactic'].isin(tactics))
net_related = (df.loc[filt, ['tactic', 'techniqueID', 'comment', 'metadata']]) # create a new filtered dataframe with just these columns

