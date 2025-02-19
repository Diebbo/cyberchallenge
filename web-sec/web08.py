import requests

url = 'http://web-08.challs.olicyber.it/login'
data = {
    'username': 'admin',
    'password': 'admin'
}
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

try:
    res = requests.post(url, headers=headers, data=data)
    res.raise_for_status()  # Raises an exception for 4XX/5XX status codes
    print(f"Status Code: {res.status_code}")
    print(res.text)

    # If you need to handle cookies/session
    print("Cookies:", res.cookies)
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
