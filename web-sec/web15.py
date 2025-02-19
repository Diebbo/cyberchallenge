#!/bin/env python3
import requests as r
import re
from bs4 import BeautifulSoup

url = 'http://web-15.challs.olicyber.it/'

page = r.get(url)

# cercare fra le risorse
soup = BeautifulSoup(page.text, 'html.parser')
resources = soup.find_all('link')
for resource in resources:
    print(resource.get('href'))
    # search for flag in the files
    res = r.get(url + resource.get('href'))
    flag = ''.join(re.findall(r'flag{(.+?)}', res.text))
    if flag:
        print(flag)
        break

# anche negli script
scripts = soup.find_all('script')
for script in scripts:
    print(script.get('src'))
    # search for flag in the files
    res = r.get(url + script.get('src'))
    flag = ''.join(re.findall(r'flag{(.+?)}', res.text))
    if flag:
        print(flag)
        break
