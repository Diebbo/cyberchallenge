#!/usr/bin/python3

import string
import base64

# from secret import KEY

def encrypt(clear, key):
  enc = []
  for i in range(len(clear)):
    key_c = key[i % len(key)]
    enc_c = chr((ord(clear[i]) + ord(key_c)) % 128)
    enc.append(enc_c)
  return str(base64.urlsafe_b64encode("".join(enc).encode('ascii')), 'ascii')

# For debug purpose
def decrypt(enc, key):
    dec = []
    enc = str(base64.urlsafe_b64decode(enc.encode('ascii')), 'ascii')
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((128 + ord(enc[i]) - ord(key_c)) % 128)
        dec.append(dec_c)
    return "".join(dec)
 
# assert(len(KEY) == 8)
# assert(all(c in string.ascii_lowercase for c in KEY))

# print("flag: CCIT{%s}" % KEY)
#
# k1 = KEY[0:4]
# k2 = KEY[4:8]
#
# m = "See you later in the city center"
# d = encrypt(m, k1)
# c = encrypt(d, k2)
#
# print("Message:", m)
# print("Ciphertext:", c)


'''
m = "See you later in the city center"
c = "QSldSTQ7HkpIJj9cQBY3VUhbQ01HXD9VRBVYSkE6UWRQS0NHRVE3VUQrTDE="
'''

def analyze_encryption(plaintext, ciphertext):
    # Decode base64 ciphertext
    decoded = str(base64.urlsafe_b64decode(ciphertext.encode('ascii')), 'ascii')
    
    # We know:
    # First encryption: c1 = (p + k1) % 128
    # Second encryption: c2 = (c1 + k2) % 128
    # Where c2 is our decoded ciphertext
    
    # For each position in the 4-char key pattern
    k1_possibilities = [set(string.ascii_lowercase) for _ in range(4)]
    k2_possibilities = [set(string.ascii_lowercase) for _ in range(4)]
    
    for i in range(len(plaintext)):
        p = ord(plaintext[i])      # plaintext char
        c2 = ord(decoded[i])       # final ciphertext char
        pos = i % 4                # position in the key (0-3)
        
        # For each possible k1 character at this position
        current_k1_possibilities = set()
        current_k2_possibilities = set()
        
        # Try each possible first key character
        for k1c in string.ascii_lowercase:
            k1_val = ord(k1c)
            # First encryption result
            c1 = (p + k1_val) % 128
            
            # For this c1, try each possible second key character
            for k2c in string.ascii_lowercase:
                k2_val = ord(k2c)
                # Second encryption result
                c2_calculated = (c1 + k2_val) % 128
                
                # If this combination produces our target ciphertext char
                if c2_calculated == c2:
                    current_k1_possibilities.add(k1c)
                    current_k2_possibilities.add(k2c)
                    #print(f"Found possible key at position {pos}: {k1c} {k2c}")
        
        # Update possibilities for this position
        k1_possibilities[pos] &= current_k1_possibilities
        k2_possibilities[pos] &= current_k2_possibilities
        
        # If any position has no possibilities, the key is impossible
        if not k1_possibilities[pos] or not k2_possibilities[pos]:
            print(f"Key is impossible at position {pos}")
            return []

        print(f"Position {pos} possibilities: {k1_possibilities[pos]} {k2_possibilities[pos]}")
    
    # Generate possible keys from remaining possibilities
    k1_candidates = [''.join(chars) for chars in itertools.product(
        *[list(pos) for pos in k1_possibilities]
    )]
    
    k2_candidates = [''.join(chars) for chars in itertools.product(
        *[list(pos) for pos in k2_possibilities]
    )]

    print(k1_candidates)
    print(k2_candidates)
    
    # Validate the keys
    valid_keys = []
    for k1 in k1_candidates:
        for k2 in k2_candidates:
            intermediate = encrypt(plaintext, k1)
            if encrypt(intermediate, k2) == ciphertext:
                valid_keys.append((k1, k2))
    
    return valid_keys

import itertools

# Known values
m = "See you later in the city center"
c = "QSldSTQ7HkpIJj9cQBY3VUhbQ01HXD9VRBVYSkE6UWRQS0NHRVE3VUQrTDE="

# Analyze
keys = analyze_encryption(m, c)
# Print all valid key combinations
for k1, k2 in keys:
    print(f"Found key: CCIT{{{k1}{k2}}}")
