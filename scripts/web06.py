#!/bin/python3

import requests

# get tocken session
URL = 'http://web-06.challs.olicyber.it/token'

URL2 = 'http://web-06.challs.olicyber.it/flag'

session = requests.Session()

response = session.get(URL)

response = session.get(URL2)

print(response.text)
