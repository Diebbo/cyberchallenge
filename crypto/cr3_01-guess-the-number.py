from pwn import *
import re

# Connect to the server
r = remote("gtn1.challs.cyberchallenge.it", 9060)

# Receive initial prompt and extract parameters
data = r.recvuntil(b"v[0] = ")
print(f"Received data: {data}")

# Extract values using robust regex patterns
m_match = re.search(br"m\s*=\s*(\d+)", data)
c_match = re.search(br"c\s*=\s*(\d+)", data)
n_match = re.search(br"n\s*=\s*(\d+)", data)
s_match = re.search(br"s\s*=\s*(\d+)", data)

if not all([m_match, c_match, n_match, s_match]):
    print("Error extracting values from the received data.")
    r.close()
    exit(1)

m = int(m_match.group(1))
c = int(c_match.group(1))
n = int(n_match.group(1))
s = int(s_match.group(1))
print(f"m: {m} c: {c} n: {n} s: {s}")

# Generate and send v[0]
v = [0] * 50
v[0] = (m * s + c) % n
print(f"v[0]: {v[0]}")
r.sendline(str(v[0]).encode())

# Generate and send subsequent values
for i in range(1, 50):
    try:
        # Wait for server prompt
        data = r.recvuntil(f"v[{i}] = ".encode())
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
