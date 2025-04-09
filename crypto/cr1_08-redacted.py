#!/usr/bin/env python2.7

from Crypto.Cipher import AES
import binascii
import string
from Crypto.Util.Padding import pad


def xor_bytes(a, b):
    """XOR two byte strings of equal length."""
    return bytes([x ^ y for x, y in zip(a, b)])


# Known information
KNOWN_KEY_PREFIX = "yn9RB3Lr43xJK2"  # Last 2 bytes unknown
CHARSET = string.ascii_letters + string.digits  # Possible characters for key
MESSAGE = "AES with CBC is very unbreakable"
C2_HEX = "78c670cb67a9e5773d696dc96b78c4e0"  # Second block ciphertext
KNOWN_C1_PREFIX = "c5"  # First byte of C1
KNOWN_C1_SUFFIX = "d49e"  # Last part of C1

# Prepare plaintext blocks
P1 = MESSAGE[:16].encode()
P2 = MESSAGE[16:].encode()
print(f"P1: {P1}")
print(f"P2: {P2}")

print("🔍 Starting brute-force for key...")
potential_solutions = []

# Brute-force the last two bytes of the key
for i in CHARSET:
    for j in CHARSET:
        try:
            # Construct key candidate
            candidate_key = (KNOWN_KEY_PREFIX + i + j).encode()

            # Create cipher in ECB mode for decryption
            cipher_ecb = AES.new(candidate_key, AES.MODE_ECB)

            # Decrypt C2
            C2 = binascii.unhexlify(C2_HEX)
            decrypted_C2 = cipher_ecb.decrypt(C2)

            # Calculate C1 = P2 ⊕ D_k(C2)
            C1 = xor_bytes(P2, decrypted_C2)
            C1_hex = binascii.hexlify(C1).decode()

            # Check if the calculated C1 matches our partial knowledge
            if C1_hex.startswith(KNOWN_C1_PREFIX) and C1_hex.endswith(KNOWN_C1_SUFFIX):
                # Now calculate the IV = P1 ⊕ D_k(C1)
                decrypted_C1 = cipher_ecb.decrypt(C1)
                IV = xor_bytes(P1, decrypted_C1)

                potential_solutions.append({
                    'key': candidate_key,
                    'IV': IV,
                    'C1': C1
                })

                print(f"✅ Found potential solution:")
                print(f"Key: {candidate_key.decode()}")
                print(f"C1: {C1_hex}")
                print(f"IV (hex): {binascii.hexlify(IV).decode()}")
                print(f"IV: {IV}")

                # Verify the solution
                try:
                    cipher_cbc = AES.new(candidate_key, AES.MODE_CBC, IV)
                    padded_message = pad(MESSAGE.encode(), AES.block_size)
                    ciphertext = cipher_cbc.encrypt(padded_message)
                    expected_ciphertext = C1 + C2

                    # We can only verify if the blocks match
                    # However, padding might affect this verification
                    # if we don't know the exact padding method in the original
                    if ciphertext.startswith(C1 + C2[:len(C1)]):
                        print("⭐ Verification successful!")
                    else:
                        print("❌ Verification failed - check padding method")
                except Exception as e:
                    print(f"Verification error: {e}")
                print("-" * 50)

        except Exception as e:
            continue

print(f"Found {len(potential_solutions)} potential solutions")

if not potential_solutions:
    print("Consider checking if any constraints were missed or if the ciphertext or known values are correct.")
