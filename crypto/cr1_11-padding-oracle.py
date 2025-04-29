#!/usr/bin/env python3

import signal
import os
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from pwn import *
import string


# TIMEOUT = 300
# BLOCK_SIZE = 16
#
# assert ("FLAG" in os.environ)
# flag = os.environ["FLAG"]
# assert (flag.startswith("CCIT{"))
# assert (flag.endswith("}"))
#
# key = os.urandom(BLOCK_SIZE)
# iv = os.urandom(BLOCK_SIZE)
#
# print("Hello! Here's an encrypted flag")
# cipher = AES.new(key, AES.MODE_CBC, iv)
# print(iv.hex()+cipher.encrypt(pad(flag.encode(), BLOCK_SIZE)).hex())
#
# r = remote("padding.challs.cyberchallenge.it", 9033)
#
# d379125038227f59afb3624c4b8885e0 - 1e69cf0d5630884e15379a04a249e533756feaf5f8fa6eb0fb5f9c302d849e518889ede8fd81cfa6ed315d4b96ed2e7d
# len = 96 //2 = 48 (16*3 blocchi)

"""
    Brute force dei primi 16 byte del plaintext (posso risalire al padding)

"""


def handle():
    while True:
        try:
            dec = bytes.fromhex(
                input("What do you want to decrypt (in hex)? ").strip())
            cipher = AES.new(key, AES.MODE_CBC, dec[:BLOCK_SIZE])
            decrypted = cipher.decrypt(dec[BLOCK_SIZE:])
            decrypted_and_unpadded = unpad(decrypted, BLOCK_SIZE)
            print("Wow you are so strong at decrypting!")
        except Exception as e:
            print(e)


# if __name__ == "__main__":
#     signal.alarm(TIMEOUT)
#     handle()

# Connect to the server
r = remote("padding.challs.cyberchallenge.it", 9033)

# Get the encrypted flag
r.recvline()
data = r.recvline().strip().decode()
print(f"Received: {data}")

# Extract IV and ciphertext
iv_hex = data[:32]
ct_hex = data[32:]
iv = bytes.fromhex(iv_hex)
ct = bytes.fromhex(ct_hex)

print(f"IV: {iv_hex}")
print(f"Ciphertext: {ct_hex}")

# Split ciphertext into blocks of 16 bytes (32 hex chars)
blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
num_blocks = len(blocks)
print(f"Number of blocks: {num_blocks}")


def get_padding_oracle_result(iv, block):
    # Send our crafted message to the padding oracle
    payload = iv.hex() + block.hex()
    r.sendlineafter(b"What do you want to decrypt (in hex)? ",
                    payload.encode())
    response = r.recvline().strip()
    return b"Wow you are so strong at decrypting!" in response

# Decrypt a single block using the padding oracle


def decrypt_block(iv, block):
    intermediate = bytearray(16)  # Will hold intermediate state
    plaintext = bytearray(16)    # Will hold plaintext

    # Decrypt byte by byte, starting from the last byte
    for byte_pos in range(15, -1, -1):
        padding_value = 16 - byte_pos

        # Set known bytes to produce correct padding for all positions after byte_pos
        for i in range(byte_pos + 1, 16):
            iv_byte = intermediate[i] ^ padding_value
            iv = iv[:i] + bytes([iv_byte]) + iv[i+1:]

        # Try all possible values for the current position
        for guess in range(256):
            test_iv = bytearray(iv)
            test_iv[byte_pos] = guess

            # Check if this produces valid padding
            if get_padding_oracle_result(bytes(test_iv), block):
                # Found valid padding, calculate intermediate value
                intermediate[byte_pos] = guess ^ padding_value
                # Calculate original plaintext byte
                plaintext[byte_pos] = intermediate[byte_pos] ^ iv[byte_pos]
                print(f"Found byte {byte_pos}: {
                      chr(plaintext[byte_pos]) if 32 <= plaintext[byte_pos] <= 126 else '?'}")
                break
        else:
            print(f"Failed to find valid byte at position {byte_pos}")

    return bytes(plaintext)


# Decrypt all blocks
decrypted = b'CCIT{7h3_m057_f4m0u5_4774ck_0n_A'
# prev_block = iv
prev_block = blocks[1]

for i in range(2, num_blocks):
    block = blocks[i]
    print(f"\nDecrypting block {i+1}/{num_blocks}")
    plaintext_block = decrypt_block(prev_block, block)
    decrypted += plaintext_block
    prev_block = block
    print(f"Current flag: {decrypted}")

print("\nFinal flag:", decrypted.decode())
r.close()

# CCIT{7h3_m057_f4m0u5_4774ck_0n_AES-CBC}
