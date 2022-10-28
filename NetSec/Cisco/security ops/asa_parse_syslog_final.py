# In this script we first search for specific events in a syslog file.
# Next we construct a set of dynamically created regex patterns 
# because we use a set each regex pattern will be unique
# next we use this set to search again through a log file and see if each line has a match with any regex pattern in the set
# As the regex set grows so will the processing time increase exponentially to use with caution (i tested it with a 200MB logfile)

import re
import csv

acl="0x98e54a82"
find_uid = re.compile(r"(?P<datetime>\w{3}\s\d{2}\s\d{2}:\d{2}:\d{2}).+(?P<eventid>ASA-5-106100).+\/(?P<source>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).+\/(?P<dst>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).(?P<dstport>\d{1,5}).+(?P<uid>(%s)).+"%acl)
first_hit_log = open("uid_matches.log", 'w', encoding='utf-8')
protocol  = 'tcp' # specify if you want to search for tcp, udp or icmp traffic

with open('cisco_syslog.log', 'r', encoding='utf_8') as logfile:
    regex_set = set()
    for logentry in logfile.readlines():
        match = find_uid.match(logentry)  
        if match and re.findall(protocol, logentry, re.IGNORECASE): # i only want TCP flows
            first_hit = match.groupdict()
            source = first_hit.get('source')
            dst = first_hit.get('dst')
            dstport = first_hit.get('dstport')
            find_tcp_fin = re.compile(f".+ASA-6-302014.+{source}.+{dst}.{dstport}.+TCP FINs.+")
            regex_set.add(find_tcp_fin.pattern)
    for item in regex_set:
        first_hit_log.write(item + '\n')

first_hit_log.close()


def search_logs(regex_set):
    with open('cisco_syslog.log', 'r', encoding='utf_8') as logfile:
        temp = re.compile("|".join(regex_set))
        total = 0
        fwrules = []
        for logentry in logfile.readlines():
            match = temp.match(logentry, re.IGNORECASE)
            if match:
                traffic_flow_dict = {}
                print("we found a match..extracting source, destination and service now")
                regex = re.compile(r".+ASA-6-302014.+\:(?P<source>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).+\:(?P<dst>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).(?P<dstport>\d{1,5}).+TCP FINs.+")
                extract_flow = regex.match(logentry)
                traffic_flow = extract_flow.groupdict()
                source = traffic_flow.get('source')
                traffic_flow_dict.update({"Source IP":source})
                traffic_flow_dict.update({"Source name":f'h_{source}'})
                dst = traffic_flow.get('dst')
                traffic_flow_dict.update({"Destination IP":dst})
                traffic_flow_dict.update({"Destination Name":f'h_{dst}'})
                dstport = traffic_flow.get('dstport')
                traffic_flow_dict.update({"Service":f'tcp/{dstport}'})
                traffic_flow_dict.update({"Service Name":f'tcp_{dstport}'})           
                fwrules.append(traffic_flow_dict)

        # remove duplicates from fwrules list
        uniques = list({(v['Source IP'], v['Destination IP'], v['Service'] ):v for v in fwrules}.values())
        for dict in uniques:
            total += 1
            print(dict)
        print(f"we found this many unique traffic flow matches: {total}")
        return uniques

def asa_create_csv(regex_set):
    '''
    fwrules is a list with nested dictionaries (each dict contains key, value pairs that represent a firewall traffic flow)
    Header : Source IP,Source Name,Destination IP,Destination Name,Service,Service Name,Application Name
    Format : ip,h_ip,ip,h_ip,tcp or udp or icmp/port,tcp_port or udp_port or icmp_port,FirewallName

    '''
    fwrules = search_logs(regex_set)
    with open('asa_fwrules.csv', 'w', encoding='utf8', newline='') as csvfile:
        dict_writer = csv.DictWriter(csvfile, fwrules[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(fwrules)


asa_create_csv(regex_set)
