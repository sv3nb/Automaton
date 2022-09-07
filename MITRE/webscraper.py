# inspect element with chrome to find out the class so you can select specific elements from the HTML page
import requests, bs4
from lxml import etree
    
'''retrieves HTML from url to parse the description of the technique so we may extract useful information'''

res = requests.get('https://attack.mitre.org/techniques/T1570/')
res.raise_for_status()
technique = bs4.BeautifulSoup(res.text, 'html.parser')

# Full technique description

description = technique.find_all("div", {"class": "description-body"})
desc = technique.select('div.description-body')
mylist = [(p.get_text(strip=True)) for p in desc]
mylist[0]

# Use XPATH to extract deep nested data
# The second table of this class contains the <p> elements that describe the mitigations

dom = etree.HTML(str(technique))
root = technique.findAll('table', {'class': 'table table-bordered table-alternate mt-2'})
try:
    children = root[1].findChildren('p', recursive=True)
except IndexError:
    number = 0
else:
    number = len(children)

mitigation_list = []

# for certain (sub)techniques there is no mitigation

if number == 0:
    print("This type of attack technique cannot be easily mitigated")
elif number <= 1:
    mitigation_list.append(dom.xpath(f'//*[@id="v-attckmatrix"]/div[2]/div/div/div/table[2]/tbody/tr[{1}]/td[3]/p/text()')[0])
else:
    for i in range(1,number + 1): # added + 1 or else he misses the last mitigation.
        try:
            mitigation_list.append(dom.xpath(f'//*[@id="v-attckmatrix"]/div[2]/div/div/div/table[2]/tbody/tr[{i}]/td[3]/p/text()')[0])
        except IndexError:
            continue

[print(f"action to take: {mitigation} \n") for mitigation in mitigation_list]
