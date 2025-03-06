from pwn import *
import string

# Connect to the remote server

# Connect to the server for each request
conn = remote('padding.challs.cyberchallenge.it', 9030)


def get_encrypted(input_str):

    # Skip the initial banner
    conn.recvuntil(b'Give me the password to encrypt:')

    # Send our input
    conn.sendline(input_str.encode())

    # Get the encrypted result
    response = conn.recvline()

    # Extract the hex string
    encrypted = response.decode().strip().split(': ')[1]
    return encrypted


def decrypt_flag():
    log.info("Starting flag decryption...")
    known = ""
    block_size = 16

    # Get the encryptions for empty string and "a" to analyze
    empty_enc = bytes.fromhex(get_encrypted(""))
    a_enc = bytes.fromhex(get_encrypted("a"))

    log.info(f"Empty input encryption: {empty_enc.hex()}")
    log.info(f"'a' input encryption: {a_enc.hex()}")

    # Determine where the flag starts to overflow into a new block
    base_blocks = len(empty_enc) // block_size
    a_blocks = len(a_enc) // block_size

    if a_blocks > base_blocks:
        # The flag with padding is close to a block boundary
        log.info(f"Adding 1 byte caused overflow to a new block")

    # Try to reveal the flag byte by byte
    charset = string.printable

    # We'll try to break up to 50 characters (reasonable flag length limit)
    for i in range(50):
        log.info(f"Trying to find character at position {i+1}")

        # We need to create inputs of varying length to align the blocks properly
        pad_len = (block_size - 1 - (i % block_size)) % block_size
        base_input = "A" * pad_len

        reference_enc = bytes.fromhex(get_encrypted(base_input))
        target_block_idx = (pad_len + i) // block_size

        found = False
        for c in charset:
            test_input = base_input + known + c
            test_enc = bytes.fromhex(get_encrypted(test_input))

            # Compare the relevant block
            if test_enc[target_block_idx * block_size:(target_block_idx + 1) * block_size] == reference_enc[target_block_idx * block_size:(target_block_idx + 1) * block_size]:
                known += c
                log.success(f"Found character: {c}")
                log.info(f"Current known string: {known}")
                found = True
                break

        if not found:
            log.failure(f"No matching character found at position {i+1}")
            log.info(f"Flag might be complete or we've hit an issue")

            # Let's try some additional verification
            if known.endswith("}"):
                log.success(f"Flag appears to be complete: {known}")
                break

    return known


if __name__ == "__main__":
    log.info("Starting attack on AES-ECB padding oracle")
    flag = decrypt_flag()
    log.success(f"Recovered flag: {flag}")
