#!/usr/bin/env python3

import signal
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# TIMEOUT = 300
#
# assert ("FLAG" in os.environ)
# flag = os.environ["FLAG"]
# assert (flag.startswith("CCIT{"))
# assert (flag.endswith("}"))
#
# key = os.urandom(16)


def handle():
    while True:
        print("1. Register")
        print("2. Login")
        print("0. Exit")
        choice = int(input("> "))
        if choice == 1:
            name = input("Insert your username: ")
            if ";" in name:
                continue
            cookie = f"usr={name};is_admin=0".encode()
            iv = os.urandom(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            encrypted = cipher.encrypt(pad(cookie, 16))
            print(f"Your login token: {iv.hex()+encrypted.hex()}")
        elif choice == 2:
            token = input("Insert your token: ")
            try:
                cookie = bytes.fromhex(token[32:])
                iv = bytes.fromhex(token[:32])
                cipher = AES.new(key, AES.MODE_CBC, iv)
                pt = unpad(cipher.decrypt(cookie), 16)
                values = pt.split(b";")
                user = values[0].split(b"=")[-1].decode()
                print(f"Welcome back {user} {values[1].decode()}")
                if b"is_admin=1" in values:
                    print(f"Here is your flag {flag}")
            except:
                print("Something is wrong with your token.")


token = "502e878b46a7dcbe8145283a25c12d1c32a89b06ae69949e00065a07c71be9743511a494d1397aa7aa73ab3611238a7d"
iv = token[:32]
cookie = token[32:]
usr = ""

# usr= - len 4
# name - len X
# ;is_admin=0 - len 11
# token is -> usr= ;is_admin=0
# just 1 block

new_iv = bytes.fromhex(iv)


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


# xor the last block of the iv in order to change the is_admin=0 to is_admin=1
new_iv = xor(
    new_iv, b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01")
new_iv = new_iv.hex()
print(f"Old IV: {iv}")
print(f"New IV: {new_iv}")
print(f"Token: {new_iv}{cookie}")
