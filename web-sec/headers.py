#!/bin/python3

import requests

URL = 'http://web-03.challs.olicyber.it/flag'

headers = {
    'X-password': 'admin',
}


response = requests.get(URL, headers=headers)

print(response.text)
