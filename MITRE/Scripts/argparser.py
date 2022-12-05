# Demonstrating arg parsing with argparse/epilog

import pandas as pd
import json
import argparse
import textwrap
import numpy as np

df = pd.read_json("data/db/technique_db.json")
pd.set_option("display.max_columns", 10)
pd.set_option("display.max_rows", 100)
pd.set_option("display.max_colwidth", None)

# 
parser = argparse.ArgumentParser(
    epilog=textwrap.dedent(
        """\
         Tactic to enter from this list:
            "Reconnaissance"
            "Resource Development"
            "Initial Access"
            "Execution"
            "Persistence"
            "Privilege Escalation"
            "Defense Evasion"
            "Credential Access"
            "Discovery"
            "Lateral Movement"
            "Collection"
            "Command and control"
            "Exfiltration"
            "Impact"
         """
    )
)

parser.add_argument("--tactic", type=str, required=True)
args = parser.parse_args()

# convert lists to strings separated by ,

def try_join(l):
    try:
        return ','.join(map(str, l))
    except TypeError:
        return np.nan

df['traffic'] = [try_join(l) for l in df['traffic']]
df['protocols'] = [try_join(l) for l in df['protocols']]
df['mitigation'] = [try_join(l) for l in df['mitigation']]
filter_tactic = (df["tactic"] == args.tactic) & (df["protocols"].str.len() > 0)

final = df.loc[
    filter_tactic,
    ["id", "name", "description", "tactic", "protocols", "traffic", "mitigation"],
]
final.to_excel(f"{args.tactic}.xlsx", engine="openpyxl")
