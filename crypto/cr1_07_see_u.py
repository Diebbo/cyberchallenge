#!/usr/bin/python3

import itertools
import string
import base64


def encrypt(clear, key):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 128)
        enc.append(enc_c)
    return str(base64.urlsafe_b64encode("".join(enc).encode('ascii')), 'ascii')


def decrypt(enc, key):
    dec = []
    enc = str(base64.urlsafe_b64decode(enc.encode('ascii')), 'ascii')
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((128 + ord(enc[i]) - ord(key_c)) % 128)
        dec.append(dec_c)
    return "".join(dec)


def find_key():
    m = "See you later in the city center"
    c = "QSldSTQ7HkpIJj9cQBY3VUhbQ01HXD9VRBVYSkE6UWRQS0NHRVE3VUQrTDE="
    target_decoded = str(base64.urlsafe_b64decode(c.encode('ascii')), 'ascii')

    found_keys = []

    print("Starting search for valid keys...")

    # Try all possible k1 values
    for k1_chars in itertools.product(string.ascii_lowercase, repeat=4):
        k1 = ''.join(k1_chars)
        intermediate = encrypt(m, k1)

        # Try to find a valid k2 using recursive backtracking with early pruning
        k2 = find_valid_k2(intermediate, target_decoded)
        if k2:
            final = encrypt(intermediate, k2)
            if final == c:
                found_keys.append(k1 + k2)
                print(f"Found key: {k1 + k2}")
                print(f"Flag: CCIT{{{k1 + k2}}}")
                return k1 + k2

    return None


def find_valid_k2(intermediate_encrypted, target_decoded):

    def backtrack(current_k2, pos):
        # If we've found a complete k2
        if pos == 4:
            return current_k2

        # Try each possible character for this position
        for char in string.ascii_lowercase:
            valid = True

            # Check if this character works for all occurrences in the key pattern
            for i in range(pos, min(len(intermediate_encrypted), len(target_decoded)), 4):
                expected = target_decoded[i]
                actual = chr(
                    (ord(intermediate_encrypted[i]) + ord(char)) % 128)
                if actual != expected:
                    valid = False
                    break

            # If the character is valid for all positions, continue recursion
            if valid:
                result = backtrack(current_k2 + char, pos + 1)
                if result:
                    return result

        return None

    return backtrack("", 0)


# Run the solver
key = find_key()
if key:
    print(f"Full key found: {key}")
    print(f"FLAG: CCIT{{{key}}}")
else:
    print("No valid key found.")
