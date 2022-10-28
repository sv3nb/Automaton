# Script to login to AFA REST API and retrieve various information such as network objects, interfaces, treename, lastreport
# Function names should be lowercase, with words separated by underscores as necessary to improve readability.
# Variable names follow the same convention as function names.

from pprint import pprint
import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()
import json
import csv
import pyinputplus as pyinput
import sys


### Function Definitions ###

def afa_login(server="afaserver"):

    global afa_server
    afa_server = server                          
    url = f"https://{afa_server}/fa/server/connection/login"    
    domain = pyinput.inputStr(prompt='Input domain (leave blank for local auth): ', blank=True, blockRegexes=['SELECT', 'UNION', 'FROM'])
    user = pyinput.inputStr(prompt='Input username: ', blockRegexes=['SELECT', 'UNION', 'FROM'])
    password = pyinput.inputPassword(prompt='Input password: ', blockRegexes=['SELECT', 'UNION', 'FROM'])

    ### Proxy settings optional###
    global proxy
    proxy = {
    'http': 'http://proxyserver:port',  # e.g. http://myproxyserver.local:8080
    'https': 'http://proxyserver:port',
    }

    payload = json.dumps(                                   
        {
            "domain": domain,
            "username": user,
            "password": password
        }
        )

    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Host': afa_server
    }

    auth_response = requests.request("POST", url, headers=headers,\
    data=payload, proxies=proxy, verify=False)

    ### extract session key ###
    session_data = json.loads(auth_response.text)               
    try:
        global session_key
        session_key = session_data['SessionID']
        return session_key
    except KeyError:
        print(f'could not retrieve SessionID: {session_data}')


def get_treename():

    '''
    Retrieve device list from which we can extract various information
    When calling this URI we also need to add the session key in the cookie header or else we get a 401!
    This cookies is dynamically generated in POSTMAN or your browser so thats why the url works there but not in a script.
    '''

    try:
        assert session_key
    except NameError:
        sys.exit("please authenticate first by running afa_login()")

    fw_name = pyinput.inputStr(prompt='provide firewall name (display name): ')
    url = f"https://{afa_server}/afa/api/v1/devices?session={session_key}"
    payload={}
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Cookie': f'PHPSESSID={session_key}'
    }
    response2 = requests.request("GET", url, headers=headers, data=payload, proxies=proxy, verify=False)
    devices = json.loads(response2.content)

    for device in devices:
        if device['display_name'] == fw_name:
            treename = device.get('name')
            break
    return treename


def get_network_objects():

    '''
    Simply provide the firewall name when running the function, the rest of the arguments can be set at the beginning of this script.
    The ipaddresses key contains a list instead of a string.
    We convert it and strip out the special chars.
    '''
    try:
        assert session_key
    except NameError:
        sys.exit("please authenticate first by running afa_login()")

    fw_name = pyinput.inputStr(prompt='provide firewall name (display name): ')
    url = f"https://{afa_server}/fa/server/network_objects/read?session={session_key}&entity={fw_name}&entityType=device&size=3000"
    payload={}
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload, proxies=proxy, verify=False)
    objects = json.loads(response.content)['entitiesReponses'][0]['values']

    with open(f'{fw_name}_networkobjects.csv', mode='w', newline='', encoding='utf-8') as myfile: 
        fieldnames = ["name","ipaddresses","ipType"]
        writer = csv.DictWriter(myfile, delimiter=',', fieldnames = fieldnames)
        writer.writeheader()
        for netobject in objects:
            netobject['ipaddresses'] = (str(netobject['ipaddresses']).strip("[,],'"))
            writer.writerow(netobject)
            print(netobject)


def get_device_interfaces():

    try:
        assert session_key
    except NameError:
        sys.exit("please authenticate first by running afa_login()")

    fw_name = pyinput.inputStr(prompt='provide firewall name (display name): ')
    url = f"https://{afa_server}/afa/api/v1/interfaces?session={session_key}&entity={fw_name}&entityType=FIREWALL"

    payload={}
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Cookie': f'PHPSESSID={session_key}'
    }
    response = requests.request("GET", url, headers=headers, data=payload, proxies=proxy, verify=False)
    interfaces = json.loads(response.content)[0]['interfaces']

    with open('interface_mapping.csv', mode='w') as data:
        fieldnames = ["logicalName","hwName","ip","zoneType", "ipsBehindInterface", "id"]
        writer = csv.DictWriter(data, delimiter=',', fieldnames = fieldnames)
        writer.writeheader()
        for intf in interfaces:
            writer.writerow(intf)


def get_devices():

    try:
        assert session_key
    except NameError:
        sys.exit("please authenticate first by running afa_login()")

    url = f"https://{afa_server}/afa/api/v1/devices?session={session_key}"
    payload={}
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Cookie': f'PHPSESSID={session_key}'
    }
    response = requests.request("GET", url, headers=headers, data=payload, proxies=proxy, verify=False)
    result = json.loads(response.content)
    mydevice_list = []
    for group in result:
        for firewall in (group['firewallDataEntities']):
            if firewall["log_server"] ==  "logserverip":
                mydevice_list.append({k: firewall[k] for k in ('name', 'host_name')}) # extract a subset of the dictionary, host_name contains the actual IP
    return mydevice_list


def get_device_services():

    try:
        assert session_key
    except NameError:
        sys.exit("please authenticate first by running afa_login()")

    fw_name = pyinput.inputStr(prompt='provide firewall name (display name): ')
    url = f"https://{afa_server}/afa/api/v1/network_services?session={session_key}&entity={fw_name}&entityType=FIREWALL"
    payload={}
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Cookie': f'PHPSESSID={session_key}'
    }
    response = requests.request("GET", url, headers=headers, data=payload, proxies=proxy, verify=False)
    result = json.loads(response.content)
    return result
