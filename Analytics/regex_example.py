# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"^.+(?P<eventid>ASA-5-106100).+\/(?P<source>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).+\/(?P<dst>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).(?P<dstport>\d{1,5}).+(?P<uid>0xc1697226).+$"

test_str = ("Jan 19 10:55:14 10.157.238.252 : %ASA-5-106100: access-list Global_acl denied tcp outside/10.169.6.133(65089) -> inside/192.168.85.110(7680) hit-cnt 4 300-second interval [0xc7afbac6, 0x0]\n"
	"Jan 19 10:55:14 10.157.238.252 : %ASA-5-106100: access-list Global_acl denied tcp outside/10.169.5.115(55827) -> inside/192.168.99.100(102) hit-cnt 1 300-second interval [0xc7afbac6, 0x0]\n"
	"Jan 19 10:55:14 10.157.238.252 : %ASA-5-106100: access-list Global_acl denied tcp outside/10.169.126.98(54860) -> inside/192.168.99.1(7680) hit-cnt 4 300-second interval [0xc7afbac6, 0x0]\n"
	"Jan 19 10:55:14 10.157.238.252 : %ASA-5-106100: access-list Global_acl denied tcp outside/10.169.6.246(2264) -> inside/10.0.0.1(10001) hit-cnt 1 first hit [0xc7afbac6, 0x0]\n"
	"Jan 19 10:55:14 10.157.238.252 : %ASA-5-106100: access-list Global_acl denied tcp outside/10.169.5.115(56234) -> inside/192.168.99.100(102) hit-cnt 1 first hit [0xc7afbac6, 0x0]\n"
	"Jan 19 10:55:15 10.157.238.252 : %ASA-5-106100: access-list Global_acl permitted tcp outside/10.169.6.222(59410) -> inside/52.182.141.63(443) hit-cnt 1 first hit [0xc1697226, 0xf4286656]\n"
	"Jan 19 10:55:15 10.157.238.252 : %ASA-5-106100: access-list Global_acl permitted tcp outside/10.169.6.1(52150) -> inside/10.157.141.27(80) hit-cnt 2 300-second interval [0x9022c45, 0x7cb9ca0c]\n"
	"Jan 19 10:55:16 10.157.238.252 : %ASA-5-106100: access-list Global_acl permitted tcp outside/10.169.6.139(51341) -> inside/23.206.104.205(443) hit-cnt 1 first hit [0xc1697226, 0xf4286656]\n"
	"Jan 19 10:55:16 10.157.238.252 : %ASA-5-106100: access-list Global_acl permitted tcp outside/10.169.6.139(51342) -> inside/10.127.210.158(443) hit-cnt 1 first hit [0xc1697226, 0xf4286656]\n"
	"Jan 19 10:55:16 10.157.238.252 : %ASA-5-106100: access-list Global_acl permitted tcp outside/10.169.6.248(57286) -> inside/104.109.143.21(443) hit-cnt 1 first hit [0xc1697226, 0xf4286656]\n"
	"Jan 19 10:55:16 10.157.238.252 : %ASA-5-106100: access-list Global_acl permitted tcp outside/10.169.6.248(57287) -> inside/104.109.143.21(443) hit-cnt 1 first hit [0xc1697226, 0xf4286656]\n"
	"Jan 19 10:55:16 10.157.238.252 : %ASA-5-106100: access-list Global_acl permitted tcp outside/10.169.4.250(65443) -> inside/17.138.175.254(443) hit-cnt 1 first hit [0xc1697226, 0xf4286656]\n"
	"Jan 19 10:55:16 10.157.238.252 : %ASA-5-106100: access-list Global_acl permitted tcp outside/10.169.4.232(54249) -> inside/17.248.176.238(443) hit-cnt 1 first hit [0xc1697226, 0xf4286656]")

matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    print("\n")
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
