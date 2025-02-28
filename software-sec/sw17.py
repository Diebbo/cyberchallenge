#!/usr/bin/env python3

from pwn import *
import re

HOST = "software-17.challs.olicyber.it"
PORT = 13000

r = remote(HOST, PORT)

r.sendlineafter(b"... Invia un qualsiasi carattere per iniziare ...", b"1")

for i in range(10):

    ask = r.recvuntil(b"somma questi numeri\n")
    print(ask)

    data = r.recvline().decode()

    # remove the [ and ] characters
    data = data.replace("[", "").replace("]", "").replace(
        "\n", "").replace(" ", "")

    numbers = list(map(int, data.split(",")))

    s = sum(numbers)
    print(numbers)
    print(s)

    r.sendline(str(s).encode())

print(r.recvall())
r.close()
