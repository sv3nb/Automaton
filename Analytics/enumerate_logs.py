# This Script will look for folders containing _output at the end.
# For each such folder that it finds it will then create a FW dictionary that represent the folder as an object in python.
# For each file with the .log extension it will then add that file to a dictionary key.
# Finally each FW dictionary is then appended to a list called LOGFILES so we can iterate over each dictionary

import typing as ty
import re, os
from pathlib import Path

CURRENTDIR = os.getcwd()
LOGFILES = []

for path in Path(CURRENTDIR).rglob('*_output'):
    FW = {}
    for logfile in Path(path.name).rglob('*.log'):
        if (re.search(r'.+_tcp\.log', logfile.name)) is not None:
            FW['tcp'] = (re.search(r'.+_tcp\.log', logfile.name)).string
        if (re.search(r'.+_udp\.log', logfile.name)) is not None:
            FW['udp'] = (re.search(r'.+_udp\.log', logfile.name)).string
        if (re.search(r'.+_icmp\.log', logfile.name)) is not None:
            FW['icmp'] = (re.search(r'.+_icmp\.log', logfile.name)).string
        continue
    LOGFILES.append(FW)
