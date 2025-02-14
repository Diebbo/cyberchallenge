import base64
import gzip
import binascii

hex = """1f 8b 08 00 71 03 60 62 00 03 ed d1 41 0a c2 30
10 85 e1 ac 3d 45 bc 80 cc 34 89 5d 2b 78 8e 10
84 ba 11 0b 69 84 16 e9 dd 0d 82 1b 11 5d 15 11
fe 6f f3 06 66 f3 98 e9 ce e9 b4 29 63 31 0b 92
6a eb fd 23 ab d7 14 f1 62 d4 37 ae 4e 1a a4 35
a2 da a8 18 2b 4b 96 7a ba 0e 25 65 6b 4d ee fb
8f 47 f8 b6 ff 53 5d fd ff 6d 3f 15 17 e2 61 6c
f3 ee 58 54 2e 51 87 e8 52 98 d6 f3 ea d7 fd 00
00 00 00 00 00 00 00 00 00 00 00 00 00 ef dd 01
48 a5 cf b9 00 28 00 00
"""

hex = hex.replace("   ", " ")
hex = hex.replace("  ", " ")
hex = hex.replace(" ", "")
hex = hex.replace("\n", "")

# decompress

data = binascii.unhexlify(hex)

data = gzip.decompress(data)

print(data)
