#!/usr/bin/env python3
import requests

url = 'http://web-10.challs.olicyber.it/'

res = requests.options(url)

print(res.headers)

print(requests.get(url).text)
