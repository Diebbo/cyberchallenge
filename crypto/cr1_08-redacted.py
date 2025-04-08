#!/usr/bin/env python2.7

"""
KEY = "yn9RB3Lr43xJK2██".encode()
IV  = "████████████████".encode()
msg = "AES with CBC is very unbreakable".encode()

aes = AES.new(KEY, AES.MODE_CBC, IV)
print binascii.hexlify(aes.encrypt(msg)).decode()

# output:
# c5██████████████████████████d49e78c670cb67a9e5773d696dc96b78c4e0
"""

from Crypto.Cipher import AES
import binascii
import string
from Crypto.Util.Padding import pad


def xor_bytes(a, b):
    """XOR two byte strings of equal length."""
    return bytes([x ^ y for x, y in zip(a, b)])


# Known information
KNOWN_KEY_PREFIX = "yn9RB3Lr43xJK2"  # Last 2 bytes unknown
CHARSET = string.ascii_letters + string.digits  # Avoid control chars
MESSAGE = "AES with CBC is very unbreakable"
FINAL_BLOCK_CIPHERTEXT_HEX = "78c670cb67a9e5773d696dc96b78c4e0"
INITIAL_CIPHERTEXT_FIRST_BYTE = b"c5"
INITIAL_CIPHERTEXT_LAST_BYTES = b"d49e"

# Padding the message manually
P2 = MESSAGE[-16:].encode()
P1 = MESSAGE[:16].encode()
print(f"P2: {P2}")
print(f"Final block ciphertext: {FINAL_BLOCK_CIPHERTEXT_HEX}")
print(f'first byte: {INITIAL_CIPHERTEXT_FIRST_BYTE}')

possible_ivs = []
print("🔍 Inizio brute-force...")

found = False
for i in CHARSET:
    for j in CHARSET:
        try:
            # Construct key
            candidate_key = (KNOWN_KEY_PREFIX + i + j).encode()
            cipher = AES.new(candidate_key, AES.MODE_ECB)

            # Extract the last ciphertext block
            C2 = binascii.unhexlify(FINAL_BLOCK_CIPHERTEXT_HEX)

            # Step 1: decrypt C3
            D_C2 = cipher.decrypt(C2)

            # Step 2: compute C2 = D_k(C3) XOR P3
            C1 = xor_bytes(D_C2, P1)

            # print(f'found C1: {C1}')
            if C1.startswith(INITIAL_CIPHERTEXT_FIRST_BYTE):
                print('something going on...')
                if C2.endswith(INITIAL_CIPHERTEXT_LAST_BYTES):
                    print('wow')
                print("\n✅ Chiave trovata!")
                print("Key: {}".format(candidate_key))
                print("C2: {}".format(binascii.hexlify(C2)))
                print("D_k(C2): {}".format(binascii.hexlify(D_C2)))
                found = True

                # find the iv
                middle = cipher.decrypt(C1)
                iv = xor_bytes(middle, P1)
                possible_ivs.append(iv)

        except Exception as e:
            continue

if not found:
    print("❌ Nessuna chiave trovata.")
else:
    print("🔑 Possibili IV trovati:")
    for iv in possible_ivs:
        # verifichiamo cifrino il messaggio
        cipher = AES.new(candidate_key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(padded)
        print("Ciphertext: {}".format(binascii.hexlify(ciphertext)))
        print("IV: {}".format(binascii.hexlify(iv)))
