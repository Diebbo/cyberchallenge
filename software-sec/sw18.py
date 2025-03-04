#!/usr/bin/env python3

from pwn import *
import re

HOST = "software-18.challs.olicyber.it"
PORT = 13001

r = remote(HOST, PORT)

r.sendlineafter(b"... Invia un qualsiasi carattere per iniziare ...", b"1")

try:
    for _ in range(100):
        # Ricevi tutto in un'unica chiamata
        ask = r.recvuntil(b"-bit\n").decode()
        print(ask)

        # Trova "0x" e convertilo in numero
        num = int(re.search(r"0x[0-9a-f]+", ask).group(), 16)

        n = int(ask[-7:-5])

        print("Data:", num)
        print("Bit:", n)

        # Packing diretto
        res = p32(num) if n == 32 else p64(num)

        r.send(res)  # Invio immediato
finally:
    print(r.recvline())
    print(r.recvline())
    r.close()
