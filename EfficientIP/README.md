# Working with the EfficientIP (SolidServer) API
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
