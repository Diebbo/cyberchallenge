#!/usr/bin/env python3

import signal
import os
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from pwn import *


TIMEOUT = 300
BLOCK_SIZE = 16

assert ("FLAG" in os.environ)
flag = os.environ["FLAG"]
assert (flag.startswith("CCIT{"))
assert (flag.endswith("}"))

key = os.urandom(BLOCK_SIZE)
iv = os.urandom(BLOCK_SIZE)

print("Hello! Here's an encrypted flag")
cipher = AES.new(key, AES.MODE_CBC, iv)
print(iv.hex()+cipher.encrypt(pad(flag.encode(), BLOCK_SIZE)).hex())

r = remote("padding.challs.cyberchallenge.it", 9033)

# d379125038227f59afb3624c4b8885e0 - 1e69cf0d5630884e15379a04a249e533756feaf5f8fa6eb0fb5f9c302d849e518889ede8fd81cfa6ed315d4b96ed2e7d
# len = 96 //2 (16*3 blocchi)

"""
    Brute force dei primi 16 byte del plaintext (posso risalire al padding)

"""


def handle():
    while True:
        try:
            dec = bytes.fromhex(
                input("What do you want to decrypt (in hex)? ").strip())
            cipher = AES.new(key, AES.MODE_CBC, dec[:BLOCK_SIZE])
            decrypted = cipher.decrypt(dec[BLOCK_SIZE:])
            decrypted_and_unpadded = unpad(decrypted, BLOCK_SIZE)
            print("Wow you are so strong at decrypting!")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    handle()
