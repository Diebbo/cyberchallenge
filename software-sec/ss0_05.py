#!/usr/bin/env python3
from pwn import *
import re

HOST = "piecewise.challs.cyberchallenge.it"
PORT = 9110

r = remote(HOST, PORT)

while True:
    ask = r.recvline().decode()
    print(ask)

    if "send me an empty line" in ask:
        r.sendline()
        continue

    # Extract number
    num_match = re.search(r"number ([0-9]+)", ask)
    if not num_match:
        print("Couldn't find number in prompt")
        continue

    num = int(num_match.group(1))

    # Extract bit size
    bit_match = re.search(r"(\d+)-bit", ask)
    if not bit_match:
        print("Couldn't find bit size in prompt")
        continue

    n = int(bit_match.group(1))  # Convert to integer

    # Extract endianness
    endian_match = re.search(r"(little|big)-endian", ask)
    if not endian_match:
        print("Couldn't find endianness in prompt")
        continue

    endian = endian_match.group(1)  # Just "little" or "big"

    print("Data:", num)
    print("Bit:", n)
    print("Endian:", endian)

    # Pack according to bit size
    if n == 32:
        res = p32(num, endian=endian)
    else:  # Assume 64-bit
        res = p64(num, endian=endian)

    r.send(res)  # Send without newline

    # Try to receive response
    try:
        response = r.recvline().decode()
        print(response)
        if "} " in response:
            print("Found flag:", response)
            break
    except:
        print("No immediate response or connection closed")

# In case we exit the loop without finding the flag
r.interactive()
