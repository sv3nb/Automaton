# This script is to retrieve data from the SolidServer IPAM service 
import requests
import json
import logging
import os
from secrets import secrets
requests.packages.urllib3.disable_warnings()

# Create logger

if not os.path.exists('.\log'):
    os.makedirs('.\log')
filename = ".\log\issues.log"
logging.basicConfig(filename=filename, level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger()


def get_subnet_list():

    '''
    Retrieves a list of objects from the ip_block_subnet_list service.
    You can use the WHERE, ORDERBY clauses as well as offset and limit.
    Example: WHERE=parent_subnet_name%20like%20'IEDU01%3ADublin'
    
    '''
    host = "https://EfficientIP"
    service = "/rest/ip_block_subnet_list"
    params = "?WHERE=vlmvlan_vlan_id!=0 or subnet_name like 'Azure-westeu-webapp001'"
    url = f'{host}{service}{params}'
    secret = secrets.get('authkey')
    proxies = {
    'http': 'http://server:port',
    'https': 'http://server:port',
    }
    payload={}
    headers = {
    'Authorization': secret,
    'Host': 'EfficientIP'
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload, verify=False, proxies=proxies)

    except Exception:
        logger.debug(f'unable to establish a connection to {url}')
        print(f'an error was encountered, please check {filename}')

    else:
        subnets = json.loads(response.content)
        with open('.\cidr.json') as f:
            cidr_list = json.load(f)['cidr']

        '''create custom list with just the data we need
        and match the subnet_size with proper CIDR notation'''

        subnet_list = []
        for net_object in subnets:
            network = {}                                                # for every object of type "subnet" we construct a new network object
            block_size = net_object['subnet_size']
            for k, v in cidr_list.items():  
                if k == block_size:
                    cidr_suffix = v
                    subnet = net_object['start_hostaddr'] + cidr_suffix
                    network['subnet'] = subnet
                    break
            network['network_name'] = net_object['subnet_name']
            network['parent'] = net_object['parent_subnet_name']
            network['vlan_id'] = net_object['vlmvlan_vlan_id']
            if 'subnet' in network:
                subnet_list.append(network)

        '''now that we have our list lets dump this into a json file.
        The previous if statement is to avoid list items with missing subnet key
        Otherwise this causes a KeyError when we run generate_xls.py'''

        with open('data\subnet_list.json', 'w') as dest_file:
            json.dump(subnet_list, dest_file, indent=4)

if __name__ == "__main__":
    get_subnet_list()