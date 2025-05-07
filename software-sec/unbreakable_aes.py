#!/usr/bin/env python3
import os
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python unbreakable_aes.py <input_file> <output_file>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Error: {input_file} does not exist.")
        return

    decrypt_file(input_file, output_file)
    print(f"Decrypted file saved as {output_file}")

def rol(byte, count):
    """Rotate left (inverse of the ROR operation)"""
    for _ in range(count):
        byte = ((byte << 1) & 0xff) | ((byte >> 7) & 0x1)
    return byte

def decrypt_file(input_path, output_path):
    """Decrypt a file encrypted with the described algorithm"""
    position = 0
    
    with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
        while True:
            chunk = infile.read(16)
            if not chunk:
                break
                
            decrypted_chunk = bytearray()
            for byte in chunk:
                position += 1
                # Rotate left by position count to reverse the ROR operation
                decrypted_byte = rol(byte, position)
                decrypted_chunk.append(decrypted_byte)
            
            outfile.write(decrypted_chunk)
if __name__ == "__main__":
    main()
