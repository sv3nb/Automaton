from stix2 import CompositeDataSource, Filter

import requests
from stix2 import MemoryStore, CompositeDataSource, Filter

def get_data_from_branch(domain):
    """get the ATT&CK STIX data from MITRE/CTI. Domain should be 'enterprise-attack', 'mobile-attack' or 'ics-attack'. Branch should typically be master."""
    stix_json = requests.get(f"https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/{domain}/{domain}.json").json()
    return MemoryStore(stix_data=stix_json["objects"])

src = get_data_from_branch("enterprise-attack")
g0075 = src.query([ Filter("external_references.external_id", "=", "G0075") ])[0]

t1134 = src.query([
    Filter("external_references.external_id", "=", "T1134"),
    Filter("type", "=", "attack-pattern")
])[0]