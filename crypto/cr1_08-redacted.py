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
import binascii, sys
import string

# Known information
KNOWN_KEY_PREFIX = "yn9RB3Lr43xJK2"
CHARSET = string.ascii_lowercase + string.ascii_uppercase + string.digits
MESSAGE = "AES with CBC is very unbreakable"
INITIAL_CIPHERTEXT_HEX = "c5"
FINAL_CIPHERTEXT_HEX = "d49e78c670cb67a9e5773d696dc96b78c4e0"

# Make sure the plaintext is properly padded (PKCS#7)
def pad_message(message):
    block_size = 16
    padding_length = block_size - (len(message) % block_size)
    if padding_length == 0:
        padding_length = block_size
    padding = chr(padding_length) * padding_length
    return message + padding  # Padding goes AFTER the message

padded_message = pad_message(MESSAGE)

# Debug info
print("Padded message length: {}".format(len(padded_message)))
print("Padded message hex: {}".format(padded_message))

# Function to recursively find the IV one byte at a time
def recursive_find_iv(key, iv_so_far, pos):
    if pos >= 16:
        # We've checked all positions and found a matching IV
        return iv_so_far
    
    for k in range(256):  # Try all possible byte values (0-255)
        # Create a new IV with the current byte set
        new_iv = list(iv_so_far)  # Convert to list for easier byte manipulation
        new_iv[pos] = chr(k)
        test_iv = ''.join(new_iv)
        
        # Create the cipher with current key and IV guess
        try:
            cipher = AES.new(key.encode(), AES.MODE_CBC, test_iv.encode())
            ciphertext = cipher.encrypt(padded_message)
            ciphertext_hex = binascii.hexlify(ciphertext)
            
            # For debugging - only print every 50th attempt to avoid flooding
            if k % 50 == 0:
                print("Trying IV pos {}: byte={}, IV={}".format(
                    pos, hex(k), binascii.hexlify(test_iv)))
                print("Ciphertext: {}".format(ciphertext_hex))
            
            # Check if the ciphertext matches our known parts
            if (ciphertext_hex.startswith(INITIAL_CIPHERTEXT_HEX) and 
                ciphertext_hex.endswith(FINAL_CIPHERTEXT_HEX)):
                print("\nFOUND MATCH!")
                print("Key: {}".format(binascii.hexlify(key)))
                print("IV: {}".format(binascii.hexlify(test_iv)))
                print("Full ciphertext: {}".format(ciphertext_hex))
                return test_iv
                
            # Optional: If we're finding partial matches, you could add more checks here
            # For example, if more ciphertext fragments are known
            
        except Exception as e:
            print("Error with IV attempt: {}".format(e))
    
    # If we've tried all values for this position and found nothing, return None
    return None

# Progress counter
total_keys = len(CHARSET) * len(CHARSET)
key_count = 0

# Main loop to try different key combinations
for i in CHARSET:
    for j in CHARSET:
        key_count += 1
        key = KNOWN_KEY_PREFIX + i + j
        
        # Convert key to proper format for AES
        key_bytes = key
        
        # Only print progress occasionally to avoid flooding
        if key_count % 20 == 0 or key_count == 1:
            print("\nTrying key {}/{}: {}".format(key_count, total_keys, key))
        
        # Start with all zeros for IV
        iv_start = '\x00' * 16
        
        # Try to find a matching IV for this key
        found_iv = recursive_find_iv(key_bytes, iv_start, 0)
        
        if found_iv:
            print("\n===== SOLUTION FOUND! =====")
            print("Key: {}".format(key))
            print("IV: {}".format(binascii.hexlify(found_iv)))
            
            # Double check the result
            cipher = AES.new(key_bytes, AES.MODE_CBC, found_iv)
            final_ciphertext = cipher.encrypt(padded_message)
            print("Final ciphertext: {}".format(binascii.hexlify(final_ciphertext)))
            sys.exit(0)  # Exit on success

print("No solution found")
