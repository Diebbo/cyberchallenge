#!/usr/bin/env python3

import struct
"""
Function to reverse to get the flag:
00001169    {
00001169        char* input = arg1;
00001179        char* flag = arg2;
0000118a        int32_t curr_position = len + (int32_t)*(uint8_t*)input;
0000118a        
00001195        if (*(uint32_t*)flag < 0)
00001195        {
000011c5            printf("Well done: your flag is indeed C…", input);
000011b7            exit(0);
000011b7            /* no return */
00001195        }
00001195        
000011c5        if (curr_position == *(uint32_t*)flag)
000011c5        {
000011c7            flag = &flag[4];
000011cc            input = &input[1];
000011e2            checker(input, flag, (uint64_t)curr_position);
000011c5        }
000011c5        
0000120c        return checker(input, flag, (uint64_t)(curr_position - (int32_t)*(uint8_t*)input));
00001169    }
"""


# Raw hex dump (little-endian encoded 4-byte integers)
B = """54 00 00 00 c3 00 00 00 22 01 00 00 8b 01 00 00 df 01 00 00 44 02 00 00 b6 02 00 00 ea 02 00 00 5e 03 00 00 c3 03 00 00 22 04 00 00 8b 04 00 00 c0 04 00 00 1f 05 00 00 87 05 00 00 dc 05 00 00 49 06 00 00 aa 06 00 00 f8 06 00 00 57 07 00 00 cb 07 00 00 fb 07 00 00 5a 08 00 00 cc 08 00 00 ff 08 00 00 42 09 00 00 b7 09 00 00 09 0a 00 00 7c 0a 00 00 e1 0a 00 00 40 0b 00 00 a4 0b 00 00 d5 0b 00 00 4b 0c 00 00 b4 0c 00 00 22 0d 00 00 87 0d 00 00 ff ff ff ff"""

# Convert hex string into a byte array
B = bytes.fromhex(B)

# Read 4 bytes at a time (little-endian)
flag = ""
for i in range(0, len(B), 4):
    value = struct.unpack("<I", B[i:i+4])[0]  # Read as little-endian integer
    if value == 0xFFFFFFFF:
        break  # End of flag

    decoded_char = value - 0x69  # Apply the assumed transformation

    # Ensure valid ASCII range
    if 0 <= decoded_char <= 0x7F:
        flag += chr(decoded_char)
    else:
        print(f"Warning: Unexpected value {decoded_char} at index {i}")

print("Recovered flag:", flag)
