# when IndexError is encountered and number=0 the mitigation_list is empty, and it skips setting the desc and mitigation for some reason.
# When the technique web page has a list of procedures listed using the 'table table-bordered table-alternate mt-2' we need the second table so root[1]
# if there is only one table with this class it is root[0]
# add the URL that you wish to troubleshoot

import requests
import bs4
from lxml import etree

url = "https://attack.mitre.org/techniques/T1548/004/"
res = requests.get(url)
res.raise_for_status()
technique = bs4.BeautifulSoup(res.text, "html.parser")
desc = technique.select("div.description-body")
mylist = [(p.get_text(strip=True)) for p in desc]
# Retrieve the migitation
dom = etree.HTML(str(technique))
root = technique.findAll(
    "table", {"class": "table table-bordered table-alternate mt-2"}
)
###problematic code starts here##################
try:
    children = root[1].findChildren("p", recursive=True)
    number = len(children)
    table_nr = 2
except IndexError:
    if len(root) != 0:
        children = root[0].findChildren("p", recursive=True)
        number = len(children)
        table_nr = 1
    else:
        number = 0

mitigation_list = (
    []
)  # when IndexError is encountered and number=0 the mitigation_list is empty, and it skips setting the desc and mitig
# for certain (sub)techniques there is no mitigation
if number == 0:
    print("This type of attack technique cannot be easily mitigated")
elif number == 1:
    mitigation_list.append(
        dom.xpath(
            f'//*[@id="v-attckmatrix"]/div[2]/div/div/div/table[{table_nr}]/tbody/tr[1]/td[3]/p/text()'
        )[0]
    )
else:
    for i in range(
        1, number + 1
    ):  # added + 1 or else the script omits the last mitigation.
        try:
            mitigation_list.append(
                dom.xpath(
                    f'//*[@id="v-attckmatrix"]/div[2]/div/div/div/table[{table_nr}]/tbody/tr[{i}]/td[3]/p/text()'
                )[0]
            )
        except IndexError:
            continue

"""example of a working first mitigation:        //*[@id="v-attckmatrix"]/div[2]/div/div/div/table[2]/tbody/tr[1]/td[3]/p/text()
example of a 'broken' first mitigation          //*[@id="v-attckmatrix"]/div[2]/div/div/div/table[1]/tbody/tr/td[3]/p/text() """
