# This is an alternative approach to the original asa_syslog_parse script 
# This approach is a lot faster and uses the NamedTuple data structure which is a sort of hybrid between a Tuple and a dictionary
# The regex patterns are tricky because the exact ASA syslog structure is not consistent and changes

import typing as ty
import re


class Connection(ty.NamedTuple):
    source: str
    dst: str
    dstport: int

acl="0x98e54a82"
find_tcp_fin = re.compile(r".+ASA-6-302014:.+:(?P<source>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/.+?(?P<dst>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.+)\/(?P<dstport>\d{1,5}).+TCP FINs.+")
find_uid = re.compile(r"(?P<datetime>\w{3}\s\d{2}\s\d{2}:\d{2}:\d{2}).+(?P<eventid>ASA-5-106100).+\/(?P<source>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).+\/(?P<dst>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).(?P<dstport>\d{1,5}).+(?P<uid>(%s)).+"%acl)

def find_tcp_conn():
    
    tcp_logfile = ".\curate_output\myfile_tcp.log"
    conn = set()
    with open(tcp_logfile, "r") as fp:
        for line in fp:
            m1 = find_uid.match(line)
            if m1:
                conn.add(Connection(m1.group("source"), m1.group("dst"), m1.group("dstport")))
                continue
            m2 = find_tcp_fin.match(line)
            if m2:
                end_conn = Connection(m2.group("source"), m2.group("dst"), m2.group("dstport"))
                if end_conn in conn:
                    yield end_conn
                    conn.remove(end_conn)
tcp_rules = []
for end_conn in find_tcp_conn():
    tcp_rules.append(end_conn._asdict())

unique_tcp_flows = list({(v['source'], v['dst'], v['dstport'] ):v for v in tcp_rules}.values())
for flow in unique_tcp_flows:
    print(flow)
 
# Sample output: {'source': '10.169.3.48', 'dst': '17.188.135.38', 'dstport': '443'}
