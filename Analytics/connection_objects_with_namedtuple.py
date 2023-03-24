from collections import namedtuple
import regex as re

# Using the collection module' namedtuple factory function to create a connection object from a list of strings

connection_log = [
    "src.ip=10.5.103.4 src.port=45558 dst.ip=172.16.50.100 dst.port=443",
    "src.ip=192.168.1.45 src.port=64585 dst.ip=172.16.50.100 dst.port=443",
    "src.ip=10.5.103.72 src.port=63254 dst.ip=172.30.4.99 dst.port=8080",
    "src.ip=10.5.103.144 src.port=65222 dst.ip=172.30.5.20 dst.port=445",
    "src.ip=10.5.103.4 src.port=49558 dst.ip=172.30.5.20 dst.port=445",
    "src.ip=10.5.103.4 src.port=45258 dst.ip=172.16.50.100 dst.port=443"
]

regex = re.compile(r"src\.ip=(?P<source>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\ssrc\.port=(?P<source_port>\d{2,5})\sdst.ip=(?P<destination>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\sdst\.port=(?P<destination_port>\d{2,5})")

connection = namedtuple('connection', 'source, source_port, destination, destination_port')
# example to construct an object: connection('10.5.103.5', '45143', '172.16.20.100', '80')

unique_connections = set()

for entry in connection_log:
    match = regex.match(entry)
    flow = connection(match.group("source"), match.group("source_port"), match.group("destination"), match.group("destination_port"))
    unique_connections.add(flow)

connection_list = list(unique_connections)

for conn in connection_list:
    print(f"the source IP is: {conn.source} and the destination IP is: {conn.destination}")