import csv
import logging
import os
import typing as ty
from pathlib import Path

# LOGGING

if not os.path.exists('.\log'):
    os.makedirs('.\log')

CSVFILES = set()
CURRENTDIR = os.getcwd()
for path in Path(CURRENTDIR).rglob('*.csv'):
    CSVFILES.add(path.name)


logfile = ".\log\palo_parse.log"
logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger()

'''
This code is for if files are delivered in zip format

import shutil
from pathlib import Path

logger.info("finding zip files to unzip")

currentdir = os.getcwd()
for path in Path(currentdir).rglob('*.zip'):
  zippedfile = path.name

shutil.unpack_archive(zippedfile, zippedfile.strip(".zip"))
'''

def main():
    # note: we cannot use spaces in this data type
    FWNAME = csv_file.split('.csv')[0].rstrip(".csv")
    logger.info(f"start processing data for {FWNAME}")
    
    class Connection(ty.NamedTuple):
        Source_IP: str
        Source_Name: str
        Destination_IP: str
        Destination_Name: str
        Service: str
        Service_Name: str
        Application_Name: str

    palo_logfile = csv_file
    any_allow_set = set() # store only unique flows that are allowed by any-any rule

    with open(palo_logfile) as palo_data:
        traffic_log = csv.DictReader(palo_data, delimiter=',')
        for flow in traffic_log:
            if flow['Rule'] == "Permit IP Any Any" and int(flow['Bytes Received']) > 0:
                allowed_conn = (Connection(flow['Source address'], \
                    f"h_{flow['Source address']}", \
                    flow['Destination address'], \
                    f"h_{flow['Destination address']}", \
                    f"{flow['IP Protocol']}/{flow['Destination Port']}", \
                    f"{flow['IP Protocol']}_{flow['Destination Port']}", \
                    f"{FWNAME}"
                ))
                any_allow_set.add(allowed_conn)

    # convert set with NamedTuple into a list with dictionaries -> any_allow_list  = [conn._asdict() for conn in any_allow_set]
    # {k.replace('_', ' ') : v for k, v  in conn._asdict().items()}  needed to be added to replace the '_' with ' ' in the csv headers

    any_allow_list = [{k.replace('_', ' ') : v for k, v  in conn._asdict().items()} for conn in any_allow_set]

    with open(f".\\algosec_import\{palo_logfile}", 'w', encoding='utf8', newline='') as csvfile:
            dict_writer = csv.DictWriter(csvfile, any_allow_list[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(any_allow_list)

    '''
    Sample output:
    Source IP,Source Name,Destination IP,Destination Name,Service,Service Name,Application Name
    10.17.49.34,h_10.17.49.34,10.157.179.200,h_10.157.179.200,tcp/389,tcp_389,SKFCNDALIFWL
    '''
    logger.info(f"end processing data for {FWNAME}")

for csv_file in CSVFILES:
    main()
