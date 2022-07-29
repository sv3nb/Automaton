import xlsxwriter
import re
import os
import json

# os.chdir(r"C:\..")
with open('networks.json') as f:
    networks = json.load(f)

# Create a list of subnets per security zone using keykeywords
# we also need to  create lists of keywords to perform a regex search on
# you can also put keywords in a txt file and read them in with: "office_zone = (Path('data\office.list').read_text()).split('\n')"

office_zone = ["users", "voice", "printers"]
wireless_zone = ["wireless", "wlan", "wifi"]
iot_zone = ["camera", "access", "packaging", "alarm", "sensor"]
dmz_zone = ["public", "internal", "extranet"]

# compile keywords from imported text files

keywords_office = re.compile("|".join(office_zone),re.IGNORECASE)
keywords_wireless = re.compile("|".join(wireless_zone),re.IGNORECASE)
keywords_iot = re.compile("|".join(iot_zone),re.IGNORECASE)
keywords_dmz = re.compile("|".join(dmz_zone),re.IGNORECASE)

# list comprehension: search for keywords in dictionary property

office = [network['subnet'] for network in networks if keywords_office.search(str(network['network_name']))]
wireless = [network['subnet'] for network in networks if keywords_wireless.search(str(network['network_name']))]
iot = [network['subnet'] for network in networks if keywords_iot.search(str(network['network_name']))]
dmz = [network['subnet'] for network in networks if keywords_dmz.search(str(network['network_name']))]

# Create Excel with security zone assignment for each vlan

with xlsxwriter.Workbook('zone_assigment.xlsx') as workbook:
    Networks = workbook.add_worksheet('Networks')
    bold = workbook.add_format({'bold': True})

    # create first column with zone names

    Networks.write('A1', 'zone_office', bold)
    Networks.write('A2', 'zone_wireless', bold)
    Networks.write('A3', 'zone_iot', bold)
    Networks.write('A4', 'zone_dmz', bold)
 
    # write each list of subnets to correct row
    
    Networks.write_row('B1',office)
    Networks.write_row ('B2',wireless)
    Networks.write_row ('B3',iot)
    Networks.write_row ('B4',dmz)