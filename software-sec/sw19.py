#!/usr/bin/env python3
from pwn import *

HOST = "software-19.challs.olicyber.it"
PORT = 13002

# Make sure to download the binary before running this script
exe = ELF("./sw-19")

r = remote(HOST, PORT)
r.sendlineafter(b"... Invia un qualsiasi carattere per iniziare ...", b"1")

try:
    for _ in range(20):  # Need to complete 20 steps
        # Receive the prompt line with the function name
        ask = r.recvuntil(b":").decode().strip()
        print(f"Received: {ask}")

        # Extract function name (format: "-> beef:")
        func = ask.split("-> ")[1][:-1]  # Remove the trailing ':'
        print(f"Looking for function: {func}")

        # Get the function address
        addr = exe.symbols.get(func)
        if addr is None:
            print(f"Error: Function '{func}' not found in binary!")
            break

        # Format the address as hex (without '0x' prefix)
        addr_hex = hex(addr)[2:]  # Remove '0x' prefix
        print(f"Function: {func} -> 0x{addr_hex}")

        # Send the hex address followed by a newline
        r.sendline(addr_hex.encode())

    # After completing all steps, receive the flag
    print(r.recvall().decode())

except Exception as e:
    print(f"Error: {e}")

finally:
    r.close()
