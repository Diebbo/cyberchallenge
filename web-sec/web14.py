#!/bin/env python3
import requests as r
import re

url = 'http://web-14.challs.olicyber.it/'

page = r.get(url)

# concat lettere evidenziate
flag = ''.join(re.findall(r'<!--(.+?)-->', page.text))
print("flag{" + flag + "}")
