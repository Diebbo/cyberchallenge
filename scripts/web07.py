#!/bin/python3

import requests

url = 'http://web-07.challs.olicyber.it/'

req = requests.get(url)

print(req.text)
print(req.headers)
print(requests.head(url).headers)
