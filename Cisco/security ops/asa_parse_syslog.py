# This script will parse the logs of an ASA firewall and extract 
# event_id TCP FIN = %ASA-6-302014 indicicates the traffic was allowed
# event_id TCP RST = "%ASA-6-106015" indicates the traffic was blocked by the firewall

import re
import csv
import xlsxwriter

def asa_parse_syslog():
    '''
    Parse the syslog output of the Cisco ASA firewall
    Filter on: ACL (UID) and event_id (IP/TCP flags)
    Sample syslog output:

    Jul 20 10:47:54 x.x.x.x : %ASA-6-302014: Teardown TCP connection 233646076 for MyLAN:10.69.3.11/51441 to MyTRansit:169.254.10.55/8081 duration 0:00:01 bytes 2219 TCP FINs from MyTRansit
    
    When there is regex match a dictionary will be created
    Each capturegroup value will then be used to create a key value pair.
    Finally each dictionary is appended to a list so we have a list of firewall traffic flows in essence.

    example output:
    {'eventid': 'ASA-5-106100', 'source': '10.77.142.204', 'scrport': '55932', 'dst': '8.8.8.8', 'dstport': '443', 'uid': '0x98e54a82'}
    '''
    acl="0x98e54a82"
    event_id="ASA-6-302014"
    allow="ASA-5-106100"
    tcp_reset ="ASA-6-106015"

    regex = re.compile(r"(?P<datetime>\w{3}\s\d{2}\s\d{2}:\d{2}:\d{2}).+(?P<eventid>ASA-5-106100).+\/(?P<source>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).(?P<srcport>\d{1,5}).+\/(?P<dst>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).(?P<dstport>\d{1,5}).+(?P<uid>(%s)).+"%acl)

    with open('asa_syslog_sample.log', 'r') as logfile:
        fwrules= []
        for logentry in logfile.readlines():
            match = regex.match(logentry)  
            if match:
                trafficflow_dict = {}  
                trafficflow = match.groupdict()
                eventid = trafficflow.get('eventid')
                trafficflow_dict.update({"Eventid":eventid})
                source = trafficflow.get('source')
                trafficflow_dict.update({"Source IP":source})
                trafficflow_dict.update({"Source name":f'h_{source}'})
                srcport = trafficflow.get('srcport')
                trafficflow_dict.update({"Source Port":srcport})
                dst = trafficflow.get('dst')
                trafficflow_dict.update({"Destination IP":dst})
                trafficflow_dict.update({"Destination Name":f'h_{dst}'})
                dstport = trafficflow.get('dstport')
                if re.findall('tcp', logentry, re.IGNORECASE):
                    trafficflow_dict.update({"Service":f'tcp/{dstport}'})
                    trafficflow_dict.update({"Service Name":f'tcp_{dstport}'})
                elif re.findall('udp', logentry, re.IGNORECASE):
                    trafficflow_dict.update({"Service":f'udp/{dstport}'})
                    trafficflow_dict.update({"Service Name":f'udp_{dstport}'})
                else:
                    trafficflow_dict.update({"Service":f'icmp/{dstport}'})
                    trafficflow_dict.update({"Service Name":f'icmp_{dstport}'})                   
                uid = trafficflow.get('uid')
                trafficflow_dict.update({"UID":uid})
                fwrules.append(trafficflow_dict)
    return fwrules


def asa_create_csv():
    '''
    fwrules is a list with nested dictionaries (each dict contains key, value pairs that represent a firewall traffic flow)
    Headers : Eventid,Source IP,Source Name,Destination IP,Destination Name,Service,Service Name,UID
    fwrules[0].keys() = Headers.
    '''
    fwrules = asa_parse_syslog()
    with open('cisco_fwrules.csv', 'w', encoding='utf8', newline='') as csvfile:
        dict_writer = csv.DictWriter(csvfile, fwrules[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(fwrules)

def asa_create_xls():
#in progress
  pass

if __name__ == "__main__":
    asa_create_csv()
