# Demonstration of how to iterate more than once over the same iterable object
# If you dont use itertools then the subsequent for loop iterates over an empty object
# Used Cisco ASA syslog log as an example

import itertools
import re

with open('asa_syslog_sample.log', 'r', encoding='utf_8') as logfile:
        fwrules= []
        acl="0x98e54a82"
        tcp_fin="ASA-6-302014"
        allow="ASA-5-106100"
        tcp_reset ="ASA-6-106015"
        find_uid = re.compile(r"(?P<datetime>\w{3}\s\d{2}\s\d{2}:\d{2}:\d{2}).+(?P<eventid>ASA-5-106100).+\/(?P<source>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).(?P<srcport>\d{1,5}).+\/(?P<dst>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).(?P<dstport>\d{1,5}).+(?P<uid>(%s)).+"%acl)
        it1, it2 = itertools.tee(logfile.readlines(), 2)
        for logentry in it1:
            match = find_uid.match(logentry)
            if match:
                first_hit = match.groupdict()
                source = first_hit.get('source')
                dst = first_hit.get('dst')
                dstport = first_hit.get('dstport')
                find_tcp_fin = re.compile(f"(.+(?P<eventid>ASA-6-302014).+\/(?P<source>{source}).+\/(?P<dst>{dst}).(?P<dstport>{dstport}).+)")
                for logentry2 in it2:
                    if "ASA-6-302014" in logentry2:
                        match_fin = find_tcp_fin.match(logentry2)
                        fwrules.append(logentry2)
[print(rule) for rule in fwrules]
