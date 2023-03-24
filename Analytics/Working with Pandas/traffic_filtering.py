#!/usr/bin/env python
# coding: utf-8

#Description: script to filter on services and export it to a xlsx
#Author: Sven Bracke
#Date: 2023-03-24 
#Version: 1.1

import pandas as pd
import argparse
import textwrap

# CSV EXAMPLE DATA

'''
"Sources","Destinations","Services","Comment","Name"
"10.10.5.0/24", "8.8.8.8", "udp_53", "", "google dns"
"h_100.100.5.2", "15.55.10.4", "tcp_80", "", "http exception"
"172.16.5.38", "192.168.104.2", "udp_51524", "", "dynamic udp 1"
"172.16.5.20,172.16.5.10", "192.168.104.2", "udp_49554", "", "dynamic udp 2"
"172.16.5.20,172.16.5.10", "192.168.104.2", "udp_65150", "", "dynamic udp 3"
'''

df = pd.read_csv('firewall_flows.csv')
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_colwidth', None)

parser = argparse.ArgumentParser(
    epilog=textwrap.dedent(
        """\
         Please select for what type of service you want to display flows for:
            dynamic_udp
            dynamic_tcp
            ddi
            tls
            http
         """
    )
)

parser.add_argument("--service", type=str, required=True)
args = parser.parse_args()
service = args.service

# MAP ARG TO REGEX

def determine_regex(service):
    service_to_regex = {
        "dynamic_udp": "udp_[4|5|6]\d{4}",
        "dynamic_tcp": "tcp_[4|5|6]\d{4}",
        "ddi": "udp_53|udp_67|udp_68|udp_123",
        "http": "tcp_80",
        "tls": "tcp_443"
    }
    return service_to_regex.get(service, "unknown")

selected_regex = determine_regex(service)

# FILTER DATAFRAME

flows = df[['Name','Sources', 'Destinations','Services']]
filtered = flows[flows.Services.str.contains(selected_regex, regex= True, na=False)]
filtered.to_excel(f"{args.service}.xlsx", engine="openpyxl")