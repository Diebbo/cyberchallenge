from pwn import *
import re

# Connect to the server
r = remote("gtn2.challs.cyberchallenge.it", 9061)

# Receive initial prompt and extract parameters
data = r.recvuntil(b"v[2] = ")
print(f"Received data: {data}")

v = [0] * 100

# Extract values using robust regex patterns
m_match = re.search(br"m\s*=\s*(\d+)", data)
n_match = re.search(br"n\s*=\s*(\d+)", data)
v0_match = re.search(br"v\[0\]\s*=\s*(\d+)", data)
v1_match = re.search(br"v\[1\]\s*=\s*(\d+)", data)

if not all([m_match, v0_match, n_match, v1_match]):
    print("Error extracting values from the received data.")
    print(f"m_match: {m_match}, n_match: {n_match}, v0_match: {v0_match}, v1_match: {v1_match}")
    r.close()
    exit(1)

m = int(m_match.group(1))
n = int(n_match.group(1))
v[0] = int(v0_match.group(1))
v[1] = int(v1_match.group(1))

print(f"m: {m}, n: {n}, v[0]: {v[0]}, v[1]: {v[1]}")

# Calculate the constant 
# c using the formula c = (v[1] - v[0] * m) % n
c = (v[1] - v[0] * m) % n

# send v2
v[2] = (v[1] * m + c) % n
print(f"v[2]: {v[2]}")
r.sendline(str(v[2]).encode())

# Generate and send subsequent values
for i in range(3, 52):
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
