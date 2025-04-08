#!/usr/bin/env python3
from pwn import *
import binascii

# Set up logging
context.log_level = 'info'

def oracle_query(conn, ciphertext):
    """
    Send a ciphertext to the oracle and check if padding is valid
    Returns True if padding is valid, False otherwise
    """
    try:
        conn.sendlineafter(b"What do you want to decrypt (in hex)? ", ciphertext.hex().encode())
        response = conn.recvline().strip().decode()
        return "Wow you are so strong" in response
    except EOFError:
        # Connection might be closed, reconnect
        log.warning("Connection closed, reconnecting...")
        conn = remote(HOST, PORT)
        conn.recvuntil(b"Hello! Here's an encrypted flag\n")
        conn.recvline()  # Skip the encrypted flag line
        return oracle_query(conn, ciphertext)

def decrypt_block(conn, iv, block):
    """
    Decrypt a single block using padding oracle attack
    """
    intermediate_bytes = [0] * 16
    plaintext = [0] * 16
    
    # Work on each byte position from last to first
    for byte_pos in range(15, -1, -1):
        # Padding value for this position (e.g., 01, 02, 03...)
        padding_value = 16 - byte_pos
        
        # Create a working copy of IV
        crafted_iv = bytearray(iv)
        
        # Adjust bytes we already know to produce the correct padding values
        for i in range(byte_pos + 1, 16):
            crafted_iv[i] = iv[i] ^ intermediate_bytes[i] ^ padding_value
        
        # Try all 256 possible values for the current byte
        for guess in range(256):
            crafted_iv[byte_pos] = guess
            
            # Send crafted IV + cipherblock to oracle
            test_payload = bytes(crafted_iv) + block
            
            # Check if padding is valid
            if oracle_query(conn, test_payload):
                # Found the right value!
                intermediate_bytes[byte_pos] = guess ^ padding_value
                plaintext[byte_pos] = intermediate_bytes[byte_pos] ^ iv[byte_pos]
                
                # If we're on the last byte, we need to verify it wasn't a false positive
                # (padding 0x01 could be valid from multiple values)
                if byte_pos == 15:
                    # Try another padding to verify
                    test_iv = crafted_iv.copy()
                    test_iv[14] = test_iv[14] ^ 1  # Change previous byte
                    if oracle_query(conn, bytes(test_iv) + block):
                        continue  # It was a false positive, try next value
                
                log.info(f"Position {byte_pos}: Found byte {plaintext[byte_pos]:02x} ('{chr(plaintext[byte_pos])}')")
                break
    
    return bytes(plaintext)

def main():
    global HOST, PORT
    
    # Connect to server
    conn = remote("padding.challs.cyberchallenge.it", 9033)
    
    # Get encrypted flag
    conn.recvuntil(b"Hello! Here's an encrypted flag\n")
    encrypted_data = conn.recvline().strip().decode()
    
    log.info(f"Received encrypted data: {encrypted_data}")
    
    # Extract IV and ciphertext
    iv = bytes.fromhex(encrypted_data[:32])
    ciphertext = bytes.fromhex(encrypted_data[32:])
    
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    log.info(f"Number of blocks to decrypt: {len(blocks)}")
    
    # Decrypt each block
    decrypted = b""
    prev_block = iv
    for i, block in enumerate(blocks):
        log.info(f"Decrypting block {i+1}/{len(blocks)}")
        plaintext_block = decrypt_block(conn, prev_block, block)
        decrypted += plaintext_block
        prev_block = block
    
    # Print the flag
    log.success(f"Decrypted flag: {decrypted.decode()}")
    conn.close()

if __name__ == "__main__":
    main()
