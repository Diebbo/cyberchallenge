from pwn import *
import re

# Connect to the server
r = remote("gtn3.challs.cyberchallenge.it", 9062)

# Receive initial prompt and extract parameters
data = r.recvuntil(b"v[3] = ")
print(f"Received data: {data}")

v = [0] * 100

# Extract values using robust regex patterns
n_match = re.search(br"n\s*=\s*(\d+)", data)
v0_match = re.search(br"v\[0\]\s*=\s*(\d+)", data)
v1_match = re.search(br"v\[1\]\s*=\s*(\d+)", data)
v2_match = re.search(br"v\[2\]\s*=\s*(\d+)", data)

if not all([v2_match, v0_match, n_match, v1_match]):
    print("Error extracting values from the received data.")
    print(f"v2_match: {v2_match}, n_match: {n_match}, v0_match: {v0_match}, v1_match: {v1_match}")
    r.close()
    exit(1)

n = int(n_match.group(1))
v[0] = int(v0_match.group(1))
v[1] = int(v1_match.group(1))
v[2] = int(v2_match.group(1))

print(f"n: {n}, v[0]: {v[0]}, v[1]: {v[1]}, v[2]: {v[2]}")

# calculate m and c
m = ((v[2] - v[1]) * pow(v[1] - v[0], -1, n)) % n
c = (v[1] - v[0] * m) % n

v[3] = (v[2] * m + c) % n

print(f"v[3]: {v[3]}")
r.sendline(str(v[3]).encode())

# Generate and send subsequent values
for i in range(4, 53):
    try:
        # Wait for server prompt
        data = r.recvuntil(f"v[{i}] = ".encode())
        print(f"Received data: {data}")
    except EOFError:
        print("Connection closed by the server.")
        break
    # Calculate the next value
    v[i] = (v[i-1] * m + c) % n
    print(f"v[{i}]: {v[i]}")
    r.sendline(str(v[i]).encode())


# Interact with the server
r.interactive()

# Close the connection
r.close()


# CCIT{4lm0st_t0_th3_t0p!}
