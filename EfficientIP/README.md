## 1.1 Working with the EfficientIP (SolidServer) API
The code in this dir essentially demonstrates the retrieving of data from the EfficientIP IPAM solution  
The goal is that we can manipulate the data into a desired data structure and format.
You can use this data then for various purposes such as automatically generating address objects for a firewall.

The Solidserver API provides us with a REST API so the data returned will be JSON. 
For this I devised a script that uses the Requests module, which allows us to create HTTP calls for the initial retrieval of data. Next the XlsxWriter module will be used to structure the data into an XLSX file.

For more info regarding the libraries used:
- XlsxWriter: https://xlsxwriter.readthedocs.io/
- Requests: https://docs.python-requests.org/en/latest/

There is also a python module made specifically for the SolidServer REST API. You can find the code repository here: https://gitlab.com/efficientip/solidserverrest
However, i prefer to use the requests module due to its generic nature and the fact that we can re-use the code for other projects.
A dedicated python library was made for the SolidServer REST API which you can find on Gitlab and GitHub.
https://www.efficientip.com/python-library/


## 1.2	Testing the API with Postman

Although the documentation is quite extensive it misses some proper examples, and it can be confusing at times. So, I decided to document some examples and more specifically on how to use the WHERE and other clauses so we can filter the output returned to us by the API.
The base url consists of the protocol, the IP or FQDN, /rest and the service you wish to access. E.g., https://serverip/rest/ip_block_subnet_list
The SolidServer API requires basic authentication to be used in every request. The “ip_block_subnet_list” gives us a list of all the subnet objects of the IPAM service.

We can use input parameters to:

- Filter (WHERE)
- Order (ORDERBY)
- Limit
- Offset the returned results.

Using the WHERE clause we can filter on all the output parameters, but the syntax needs to be precise, and URL encoded.
For example, we can filter on “subnet_name” or "subnet_vlan_id" and order the results.

```
/rest/ip_block_subnet_list?WHERE=subnet_name like 'Packaging'

/rest/ip_block_subnet_list?WHERE=vlmvlan_vlan_id!%3D0&ORDERBY=vlmvlan_id
```

## 1.3	Only retrieve VLAN objects

We are especially interested in retrieving all the network objects that effectively constitute individual VLANs.  
Hence, we might want to retrieve all the objects that have a VLAN ID other than 0 or null defined. 
In the API this can be done by looking at the “vlmsvlan_vlan_id” value.  
We can specify within a parameter that it should not contain a particular value. We want all the subnets with a “vlmsvlan_vlan_id” other than 0.  

Example URI with params:
```
/rest/ip_block_subnet_list?WHERE=vlmvlan_vlan_id!%3D0&ORDERBY=vlmvlan_id  

/rest/ip_block_subnet_list?WHERE=vlmvlan_vlan_id!=0 or subnet_name like 'Azure'
```
