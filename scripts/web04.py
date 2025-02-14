#!/bin/python3

import requests

URL = 'http://web-04.challs.olicyber.it/users'

headers = {
    'Accept': 'application/xml',
}

response = requests.get(URL, headers=headers)

print(response.text)
