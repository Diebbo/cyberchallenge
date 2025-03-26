#!/usr/bin/env python3
from pwn import *

# try some random str 'hjkl' format
# passed as program argument
init = ''
directions = ('h', 'j', 'k', 'l')
q = [init + i for i in directions]
while q:
    curr = q.pop(0)
    # for i in range(4):
    #     q.append(curr + directions[i])
    try:
        p = process(['./ss1_06_pacman', curr], env={'LD_PRELOAD': './fptrace.so'})
        output = p.recvall()
        print(f"Passed with {curr}")
    except EOFError:
        print(f"Crashed with {curr}")
        continue
    p.close()
