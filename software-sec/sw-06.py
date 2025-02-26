# Define the flag and key as byte strings
flag = b'\xd4\\\xdc\xbbk\x1e\xd3JJ^\xd2\xdf\xac|\x00\x00'
key = b'\xb20\xbd\xdc\x10z\xe1{,;\xe2\xec\x99\x01'

# Apply XOR byte by byte
xor_result = bytes([f ^ k for f, k in zip(flag, key)])

# Print the result
print(xor_result)
