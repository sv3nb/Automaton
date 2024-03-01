import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()
import sys
import json

#provide the IP or FQDN as argument when running the script
host = sys.argv[1]
# use the URL to match the right api_key
with open('api-key.json') as g:
    json_dict = json.load(g)
    api_key = json_dict[host]

def Get_SLA_Log(host,api_key):
    sla = "SLA_Azure"
    interface = "VPN-Azure"
    http_header = {'content-type':'application/json', 'Accept': 'application/json'}
    url = 'https://'+ host + '/api/v2/monitor/virtual-wan/sla-log?sla=' + sla + '&interface=' + interface + '&access_token=' + api_key
    payload={}
    response = requests.get(url, headers=http_header, data=payload, verify=False)

    print(response.text)


if __name__ == "__main__":
    Get_SLA_Log(host,api_key)
