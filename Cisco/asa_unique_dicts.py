# extract the unique entries based the combination of source, destination and dstport
# create cli code from this unique list of dictionaries.

rules = [
    {'eventid': 'ASA-5-106100', 'source': '10.170.142.204', 'dst': '10.5.201.195', 'dstport': '443'},
    {'eventid': 'ASA-5-106100', 'source': '10.65.142.204', 'dst': '10.5.201.195', 'dstport': '443'},
    {'eventid': 'ASA-5-106100', 'source': '10.170.142.204', 'dst': '10.5.201.195', 'dstport': '443'},
    {'eventid': 'ASA-5-106100', 'source': '10.180.142.210', 'dst': '10.5.201.195', 'dstport': '80'},
    {'eventid': 'ASA-5-106100', 'source': '10.180.142.210', 'dst': '10.5.201.195', 'dstport': '80'},
    {'eventid': 'ASA-5-106100', 'source': '10.110.142.204', 'dst': '10.5.201.195', 'dstport': '443'},
    {'eventid': 'ASA-5-106100', 'source': '10.170.142.204', 'dst': '10.5.201.195', 'dstport': '8443'},
    {'eventid': 'ASA-5-106100', 'source': '10.170.142.204', 'dst': '10.66.201.19', 'dstport': '443'},
    {'eventid': 'ASA-5-106100', 'source': '10.170.142.204', 'dst': '10.66.201.19', 'dstport': '445'},
    {'eventid': 'ASA-5-106100', 'source': '10.170.142.204', 'dst': '10.66.201.19', 'dstport': '88'}
]

uniques = list({(v['source'], v['dst'], v['dstport'] ):v for v in rules}.values())

for entry in uniques:
    print(f"access-list ACL_IN extended permit tcp {entry['source']} host {entry['dst']} eq {entry['dstport']}")
