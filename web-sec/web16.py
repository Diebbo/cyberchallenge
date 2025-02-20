#!/bin/env python3
import requests as r
import re
from bs4 import BeautifulSoup

base_url = 'http://web-16.challs.olicyber.it'

visited = []


def get_links():
    global visited
    q = [base_url]  # coda
    try:
        while q:
            url = q.pop(0)
            visited.append(url)
            print(url)

            response = r.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # search for flag
            headers = soup.find_all('h1')
            for header in headers:
                if 'flag' in header.text:
                    print(header.text)
                    return

            # goto next link
            links = soup.find_all('a')

            for link in links:
                href = link.get('href')
                if href not in visited:
                    q.append(base_url + href)
    except:
        pass


get_links()
