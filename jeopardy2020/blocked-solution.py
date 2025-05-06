from pwn import *
import json
from base64 import b64decode, b64encode
from Crypto.Cipher import AES

# Local or remote process (uncomment one of these)
r = process("./blocked.py")
# r = remote("blocked.challs.cyberchallenge.it", 9214)


def get_token(name, surname, email):
    r.recvuntil(b"> ")
    r.sendline(b"1")  # Choose "Sign-up"
    r.recvuntil(b"name: ")
    r.sendline(name)
    r.recvuntil(b"surname: ")
    r.sendline(surname)
    r.recvuntil(b"email: ")
    r.sendline(email)
    r.recvuntil(b"Here's your login token:\n")
    return r.recvline().strip()


# Step 1: Create a token where "type":"admin" appears in a known block
# We'll pad the name to push the admin field into a predictable block
admin_token = get_token(
    b'a'*10,  # Name - 10 'a's to help with alignment
    b'","type":"admin","x":"',  # Injected fields
    b'a'  # Email
)
print(f"Admin token: {admin_token}")

# Step 2: Create a normal user token to get the proper structure
user_token = get_token(
    b'a'*10,  # Same length name as above
    b'user',  # Normal surname
    b'a'  # Email
)
print(f"User token: {user_token}")

# Step 3: Extract the block containing "type":"admin" from admin_token
admin_blocks = b64decode(admin_token)
# This may need adjustment based on actual alignment
admin_block = admin_blocks[32:48]

# Step 4: Replace the corresponding block in user_token
user_blocks = bytearray(b64decode(user_token))
user_blocks[32:48] = admin_block  # Same position as above, may need adjustment
modified_token = b64encode(bytes(user_blocks))

# Step 5: Login with the modified token
r.recvuntil(b"> ")
r.sendline(b"2")  # Choose "Log-in"
r.recvuntil(b"login token: ")
r.sendline(modified_token)

# Get the flag
r.interactive()
