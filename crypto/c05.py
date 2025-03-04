def xor(a, b):
    """XOR two byte sequences. If b is shorter, it will be repeated to match length of a."""
    if len(b) == 1:
        # If key is a single byte, repeat it to match ciphertext length
        b = b * len(a)
    return bytes([x ^ y for x, y in zip(a, b)])


def decrypt(ciphertext):
    """Try all possible single-byte keys to decrypt the ciphertext."""
    cipherbytes = bytes.fromhex(ciphertext)
    possible_plaintexts = []

    for i in range(256):
        key = i.to_bytes(1, 'big')
        plaintext = xor(cipherbytes, key)

        # Try to decode as ASCII and check if it's readable
        try:
            decoded = plaintext.decode('ascii')
            # Only add printable ASCII results
            if all(32 <= ord(c) <= 126 for c in decoded):
                print(f"Key {i} (0x{i:02x}): {decoded}")
                possible_plaintexts.append((i, decoded))
        except UnicodeDecodeError:
            # Not valid ASCII, probably not the right key
            continue

    # Return possible plaintexts for further analysis
    return possible_plaintexts


# Your ciphertext
ciphertext = '104e137f425954137f74107f525511457f5468134d7f146c4c'
results = decrypt(ciphertext)

if results:
    print("\nPossible plaintexts found:")
    for key, text in results:
        print(f"Key: {key} (0x{key:02x}) -> {text}")
else:
    print("\nNo readable plaintexts found. Maybe try a different encoding.")
