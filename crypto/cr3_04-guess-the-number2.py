from pwn import *
import re
from math import gcd
from functools import reduce

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None  # modular inverse doesn't exist
    else:
        return x % m

def solve_lcg(values):
    diffs = [y - x for x, y in zip(values, values[1:])]
    zeroes = [d1*d3 - d2*d2 for d1, d2, d3 in zip(diffs, diffs[1:], diffs[2:])]
    n = abs(reduce(gcd, zeroes))
    
    m = (values[2] - values[1]) * modinv(values[1] - values[0], n) % n
    c = (values[1] - values[0] * m) % n
    
    return m, c, n

# Connect to the server
r = remote("gtn4.challs.cyberchallenge.it", 9063)

# Receive initial prompt and extract parameters
data = r.recvuntil(b"v[7] = ")
print(f"Received data: {data.decode()}")

# Extract values using regex
v = []
for i in range(7):
    match = re.search(fr"v\[{i}\]\s*=\s*(\d+)".encode(), data)
    if not match:
        print(f"Error extracting v[{i}]")
        r.close()
        exit(1)
    v.append(int(match.group(1)))

print(f"Extracted values: {v}")

# Solve for LCG parameters
try:
    m, c, n = solve_lcg(v)
    print(f"Found parameters: m={m}, c={c}, n={n}")
except Exception as e:
    print(f"Failed to solve LCG: {e}")
    r.close()
    exit(1)

# Calculate v[7]
next_val = (v[-1] * m + c) % n
print(f"Predicted v[7]: {next_val}")
r.sendline(str(next_val).encode())

# Generate and send subsequent values
for i in range(8, 60):
    try:
        # Wait for server prompt
        data = r.recvuntil(f"v[{i}] = ".encode())
        print(f"Received data: {data.decode()}")
    except EOFError:
        print("Connection closed by the server.")
        break
    
    # Calculate the next value
    next_val = (next_val * m + c) % n
    print(f"Predicted v[{i}]: {next_val}")
    r.sendline(str(next_val).encode())

# Get the flag
r.recvuntil(b"flag: ")
flag = r.recvline().decode().strip()
print(f"Flag: {flag}")

# Close the connection
r.close()


# Flag: CCIT{Y0u_kn0w_n0th1ng_J0hn_Sn0w}

