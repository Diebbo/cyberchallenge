#!/bin/env python3
import requests as r
import re

url = 'http://web-13.challs.olicyber.it/'

page = r.get(url)

# concat lettere evidenziate
flag = ''.join(re.findall(r'<span class="red">(.+?)</span>', page.text))
print("flag{" + flag + "}")
