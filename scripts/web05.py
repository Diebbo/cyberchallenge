#!/bin/python3

import requests

URL = 'http://web-05.challs.olicyber.it/flag'

headers = {
    'Accept': 'application/xml',
}

cookies = {
    'password': 'admin',
}

response = requests.get(URL, headers=headers, cookies=cookies)

print(response.text)
