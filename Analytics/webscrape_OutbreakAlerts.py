# Web scraping to extract most recent outbreak-alerts from Fortiguard website.

from bs4 import BeautifulSoup
import requests
import re

medium = "3"
high = "4"
critical = "5"

alerts = requests.get(f'https://www.fortiguard.com/outbreak-alert?risk={critical}')
soup = BeautifulSoup(alerts.text, features="html.parser")

titles = soup.findAll('div', attrs={'class':'title'})
description = soup.findAll('div', attrs={'class':'description'})
for title in titles:
    alert = {}
    alert['title'] = (title.text).strip()
    alert['description'] = (re.sub(' +', ' ', title.find_next_siblings("div", {"class": "description"})[0].text)).strip()
    print(alert)
