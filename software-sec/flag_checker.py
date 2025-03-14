import struct
from pwn import *

def decrypt_flag(hex_data):
    # Parse the hex dump into a list of integers
    values = []
    for chunk in hex_data.split():
        if chunk != '00':  # Skip empty bytes for parsing (though they matter in the real data)
            values.append(int(chunk, 16))
    
    # Properly reconstruct the 32-bit integers (little endian)
    flag_values = []
    for i in range(0, len(values), 4):
        if i+3 < len(values):
            val = values[i] | (values[i+1] << 8) | (values[i+2] << 16) | (values[i+3] << 24)
            flag_values.append(val)
    
    # If the last value isn't negative, we need to make sure we have that terminator
    if flag_values and flag_values[-1] >= 0:
        flag_values.append(-1)  # Add terminator if needed
    
    # Reverse-engineer the flag
    flag = ""
    pos = 0
    
    for i in range(len(flag_values)-1):  # Skip the last negative value
        flag_val = flag_values[i]
        
        # From the original function, we know that:
        # pos + char_value = flag_value
        # So: char_value = flag_value - pos
        char_value = flag_val - pos
        
        # Make sure it's a printable ASCII character
        if 32 <= char_value <= 126:
            flag += chr(char_value)
        else:
            # If we get a non-printable character, something is wrong
            print(f"Warning: Non-printable character ({char_value}) at position {i}")
            flag += '?'
        
        # Update position for next iteration
        pos = flag_val
    
    return flag

# Raw hex dump (original data)
B = """54 00 00 00 c3 00 00 00 22 01 00 00 8b 01 00 00 df 01 00 00 44 02 00 00 b6 02 00 00 ea 02 00 00 5e 03 00 00 c3 03 00 00 22 04 00 00 8b 04 00 00 c0 04 00 00 1f 05 00 00 87 05 00 00 dc 05 00 00 49 06 00 00 aa 06 00 00 f8 06 00 00 57 07 00 00 cb 07 00 00 fb 07 00 00 5a 08 00 00 cc 08 00 00 ff 08 00 00 42 09 00 00 b7 09 00 00 09 0a 00 00 7c 0a 00 00 e1 0a 00 00 40 0b 00 00 a4 0b 00 00 d5 0b 00 00 4b 0c 00 00 b4 0c 00 00 22 0d 00 00 87 0d 00 00 ff ff ff ff"""

# Alternative parsing approach - directly read little-endian integers
def parse_hex_dump(hex_dump):
    # Remove all whitespace and parse as a continuous hex string
    hex_string = ''.join(hex_dump.split())
    
    # Create a bytes object from the hex string
    binary_data = bytes.fromhex(hex_string)
    
    # Unpack as little-endian 32-bit integers
    flag_values = []
    for i in range(0, len(binary_data), 4):
        if i+3 < len(binary_data):
            val = struct.unpack('<i', binary_data[i:i+4])[0]
            flag_values.append(val)
    
    return flag_values

def main():
    print("[+] Attempting to reverse-engineer the flag...")
    
    # Method 1: Using the more detailed approach
    flag1 = decrypt_flag(B)
    print(f"[+] Flag (Method 1): CCIT{{{flag1}}}")
    
    # Method 2: Using direct unpacking approach
    flag_values = parse_hex_dump(B)
    
    flag2 = ""
    pos = 0
    for val in flag_values:
        if val < 0:
            break
        
        char_val = val - pos
        flag2 += chr(char_val)
        pos = val
    
    print(f"[+] Flag (Method 2): CCIT{{{flag2}}}")

if __name__ == "__main__":
    main()
