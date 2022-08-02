# Demonstration of how to iterate more than once over the same iterable object
# Used Cisco ASA syslog log as an example

import itertools

with open('cisco_syslog.log', 'r', encoding='utf_8') as logfile:
        fwrules= []
        it1, it2 = itertools.tee(logfile.readlines(), 2)
        for logentry in it1:
            if "0x51945210" in logentry:
                for logentry2 in it2:
                    if "ASA-6-302014" in logentry2:
                        print(logentry2)
