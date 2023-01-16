# Coding: utf-8
# Description: Create custom MITRE ATT&CK Technique database
# Author: Sven Bracke <sven@skrypter.be>
# Date: 2022-10-11
# Version: 1.2
# MITRE Version: 11

import requests, bs4
import re
from collections.abc import MutableMapping
import numpy as np
import json
from lxml import etree

# Definition of tactics depends on MITRE ATT&CK version

tactics = [
    {"TA0001": "Initial Access"},
    {"TA0002": "Execution"},
    {"TA0004": "Privilege Escalation"},
    {"TA0005": "Defense Evasion"},
    {"TA0006": "Credential Access"},
    {"TA0007": "Discovery"},
    {"TA0008": "Lateral Movement"},
    {"TA0009": "Collection"},
    {"TA0010": "Exfiltration"},
    {"TA0011": "Command and Control"},
    {"TA0040": "Impact"},
    {"TA0042": "Resource Development"},
    {"TA0043": "Reconnaissance"},
]

# Technique CLASS DEFINITION


class Technique(MutableMapping):

    """
    Create custom class for Technique objects enriched with metadata.

    When retrieving the migiation: the second table of the selected class
    contains the <p> elements that describe the mitigations hence we select root[1]
    and search for <p> child elements.
    """

    def get_metadata(self, url):
        # Retrieve the description
        res = requests.get(url)
        res.raise_for_status()
        technique = bs4.BeautifulSoup(res.text, "html.parser")
        desc = technique.select("div.description-body")
        mylist = [(p.get_text(strip=True)) for p in desc]
        # Retrieve the migitation
        dom = etree.HTML(str(technique))
        root = technique.findAll(
            "table", {"class": "table table-bordered table-alternate mt-2"}
        )
        try:
            children = root[1].findChildren("p", recursive=True)
            number = len(children)
            table_nr = 2
        except IndexError:
            number = 0

        mitigation_list = []
        if number == 0:
            mitigation_list.append(
                "Unable to retrieve mitigations"
            )
        elif number == 1:
            mitigation_list.append(
                dom.xpath(
                    f'//*[@id="v-attckmatrix"]/div[2]/div/div/div/table[{table_nr}]/tbody/tr[1]/td[3]/p/text()'
                )[0]
            )
        else:
            for i in range(
                1, number + 1
            ):  # added + 1 or else the script omits the last mitigation.
                try:
                    mitigation_list.append(
                        dom.xpath(
                            f'//*[@id="v-attckmatrix"]/div[2]/div/div/div/table[{table_nr}]/tbody/tr[{i}]/td[3]/p/text()'
                        )[0]
                    )
                except IndexError:
                    continue
        return mylist[0], mitigation_list

    def traffic_matcher(self, tactic):
        if tactic == "Initial Access":
            return ["From EXTERNAL To DMZ"]
        elif tactic == "Collection":
            return ["From INTERNAL To INTERNAL"]
        elif tactic == "Lateral Movement":
            return [
                "From DMZ To INTERNAL",
                "From INTERNAL To DMZ",
                "From INTERNAL To INTERNAL",
            ]
        elif tactic == "Discovery":
            return ["From INTERNAL To INTERNAL", "From DMZ To INTERNAL"]
        elif tactic == "Exfiltration":
            return ["From DMZ To EXTERNAL"]
        elif tactic == "Command and Control":
            return ["From DMZ To EXTERNAL", "From INTERNAL To EXTERNAL"]
        elif tactic == "Reconnaissance":
            return ["From EXTERNAL To DMZ", "From EXTERNAL To INTERNAL"]
        elif tactic == "Impact":
            return ["From INTERNAL To INTERNAL"]

    def __init__(self, id, name="", tactic=""):
        self.tactic = tactic
        self.id = id
        self.name = name
        self.url = f"https://attack.mitre.org/techniques/{str(id).replace('.', '/')}"
        metadata = self.get_metadata(self.url)
        self.description = metadata[0]
        self.mitigation = metadata[1]
        self.traffic = self.traffic_matcher(self.tactic)

    # Must be included in class
    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)


# Construct list with Technique objects

techniques = []

for tactic in tactics:
    tactic_url = requests.get(
        f"https://attack.mitre.org/tactics/{list(tactic.keys())[0]}/"
    )
    tactic_html = bs4.BeautifulSoup(tactic_url.text, "html.parser")
    for technique in tactic_html.find_all(
        "tr", {"class": ["technique", "sub technique"]}
    ):
        tactic_name = list(tactic.values())[
            0
        ]  # How to get dict key or value directly, works best for single key, value pairs
        links = technique.find_all("a", href=True)
        link = links[1]  # access the second <a> element which contains the name
        techniqueID = ((link["href"]).strip("/techniques/")).replace("/", ".")
        name = (link.get_text()).strip()
        techniques.append(Technique(techniqueID, name, tactic_name))

# Ensure case sensitivity does not affect matches, and check for comma's!

regex_set = [
    "FTP",
    "SMTP",
    "TFTP",
    "FTPS",
    "VPN",
    "SMB",
    "RDP",
    "RPC",
    "NetBIOS",
    "MySQL",
    "IMAP",
    "POP3",
    "SMTPS",
    "Windows Remote",
    "Kerberos",
    "WMI",
    "SQL",
    "HTTP",
    "HTTPS",
    "LDAP",
    "SNMP",
    "web services",
    "SSH",
    "Telnet",
    "TLS",
    "SFTP",
    "SCP",
    "DHCP",
    "DNS",
    "VNC",
    "RSYNC",
    "Oracle",
    "IPSEC",
    "LLMNR",
    "NTP",
    "WinRM",
    "Samba",
    "TCP.\d{2,4}",
    "UDP.\d{2,4}",
    "Port.\d{2,4}",
]
mysearch = re.compile("|".join(regex_set))

for technique in techniques:
    protocols = []
    for match in mysearch.findall(technique.description, re.IGNORECASE):
        protocols.append(match.upper())
    technique["protocols"] = protocols
    technique.protocols = np.unique(
        technique["protocols"]
    ).tolist()  # Get rid of duplicate protocols


# Save everything to Key-Value based DB

json_db = [technique.__dict__ for technique in techniques]

with open("data/db/technique_db.json", "w", encoding="utf-8") as output:
    json.dump(json_db, output, indent=4, sort_keys=True)
