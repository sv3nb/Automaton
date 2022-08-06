# Due to the size of the ASA syslog files to parse we experienced performance issues in Python
# Therefore we wanted to reduce the initial syslog file by stripping out any irrelevant data and splitting it up into multiple files
# This script will initially use 'sed' to remove any unnecessary eventid's
# then it will extract all the icmp and udp loglines to separate files and subsequently delete them in the original file
# Then we extract all the traffic flows with a TCP RST (DENY) in this script and write them to a CSV file
# Final cleanup to remove TCP RST events from the initial log file and copy the curated file to a subdir
# The challenge was to get the bash commands to work properly the key is to use different vars for the processes 

import re
import subprocess
import datetime

syslogfile = "mysyslogfile.log"

# INITIAL CLEANUP TO REDUCE UNNECESSARY FILE SIZE

print(f"Starting initial clean and splitting up of syslog file: {syslogfile}")

bashcommands = [
  f"sed -i '/ASA-6-302013/d' {syslogfile}", \
  f"sed -i '/ASA-5-304001/d' {syslogfile}", \
  f"grep -i 'icmp' {syslogfile} > ./output/myfile_icmp.log && sed -i '/icmp/Id' {syslogfile}", \
  f"grep -i 'udp' {syslogfile} > ./output/myfile_udp.log && sed -i '/udp/Id' {syslogfile}"
  ]

for command in bashcommands:
  process1 = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
  output, error = process1.communicate()

# DEFINE FUNCTION TO EXTRACT TCP RST ENTRIES

def asa_search_syslog(syslogfile):

  print(f"Start search for TCP RST entries")
  find_rst = re.compile(r".+(?P<eventid>ASA-6-106015).+Deny.+from.(?P<source>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).+to.(?P<dst>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).(?P<dstport>\d{1,5}).+")
  fwrules = []
  with open(syslogfile, 'r', encoding='utf_8') as logfile:
    for logentry in logfile.readlines():
      match_rst = find_rst.match(logentry, re.IGNORECASE)
      if match_rst:
        traffic_flow_dict = {}
        print("we found a RST..extracting source, destination and service now")
        traffic_flow = match_rst.groupdict()
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
    
    fwrules_final = list({(v['Source IP'], v['Destination IP'], v['Service'] ):v for v in fwrules}.values())
    return fwrules_final

'''
    fwrules_final is a list with nested dictionaries (each dict contains key, value pairs that represent a firewall traffic flow)
    Header : Source IP,Source Name,Destination IP,Destination Name,Service,Service Name,Application Name
    Format : ip,h_ip,ip,h_ip,tcp or udp or icmp/port,tcp_port or udp_port or icmp_port,FirewallName

'''

import csv

with open('./output/csv/asa_rules_deny.csv', 'w', encoding='utf8', newline='') as csvfile:
  fwrules_final = asa_search_syslog(syslogfile)
  try:
    print("start with creation of CSV file")
    dict_writer = csv.DictWriter(csvfile, fwrules_final[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(fwrules_final)
  except IndexError:
    pass

# FINAL CLEANUP

print("start with final clean up")
final_cleanup = f"sed -i '/ASA-6-106015/d' {syslogfile} && mv {syslogfile} ./output/myfile_tcp"
process2 = subprocess.Popen(final_cleanup, shell=True, stdout=subprocess.PIPE)
output, error = process2.communicate()

## FINISH

from datetime import datetime

now = datetime.now()
print(f"script finished at: {now}")