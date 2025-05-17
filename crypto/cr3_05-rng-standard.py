from pwn import *
import re
import random


r = remote('srng.challs.cyberchallenge.it', 9064)

while True:
    # from source => to_guess = random.getrandbits(32)
    max = 2**32 - 1
    min = 0
    # current = (max + min) // 2
    current = random.getrandbits(32)

    for i in range(10):
        r.sendlineafter(b">", b"1")
        r.sendlineafter(b">", str(current).encode())
        data = r.recvline().decode()
        match = re.search(r"My number is (higher|lower)!", data, re.IGNORECASE)
        if not match:
            r.interactive()
            r.close()
            exit(1)

        # i know if it's higher or lower -> binary search
        compare = match.group(1)
        print(f"Current: {current}, Min: {min}, Max: {max}, Compare: {compare}")
        if compare == "higher":
            min = current + 1
            current = (max + min) // 2
        elif compare == "lower":
            max = current - 1
            current = (max + min) // 2
        else:
            print("Invalid response")
            r.close()
            exit(1)
    # if we reach here, we have 10 tries    
    print(r.recvline().decode())
    print("10 done, again")

print(f"Extracted values: {v}")
