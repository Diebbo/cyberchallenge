
from pwn import *
from Crypto.Cipher import DES, AES, DES3, ChaCha20
from Crypto.Util.Padding import pad, unpad


def xor(a, key):
    """Repeating-key XOR encryption."""
    if len(key) < len(a):
        key = key * (len(a) // len(key)) + key[:len(a) % len(key)]
    return bytes([x ^ y for x, y in zip(a, b)])


def encrypt_des_cbc(key, plaintext, iv):
    cipher = DES.new(key, DES.MODE_CBC, iv)
    return cipher.encrypt(plaintext)


key_hex = '11d1cb432a4555c8'
plaintext = 'La lunghezza di questa frase non è divisibile per 8'
Padding = 'x923'

key = bytes.fromhex(key_hex)
iv = os.urandom(8)
res = encrypt_des_cbc(key, pad(plaintext.encode(), 8, style=Padding), iv)

print("1 ----")

print(f"encrypted: {res.hex()}")
print(f"iv: {iv.hex()}")


plaintext = 'Mi chiedo cosa significhi il numero nel nome di questo algoritmo.'
# Padding scheme = pkcs7 (block size = 16)
# Segment size = 24
# Cipher = AES256
# Mode = CFB

# Creazione della chiave e IV
key = os.urandom(32)  # 32 byte per AES-256 (256 bit)
iv = os.urandom(16)   # 16 byte (128 bit) per l'IV

# Applica padding PKCS7
block_size = 16
padded_plaintext = pad(plaintext.encode(), block_size, style='pkcs7')

# Creazione del cifrario con segment size di 24 bit (3 byte)
# In Pycryptodome, segment_size è in bit
cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=24)
ciphertext = cipher.encrypt(padded_plaintext)

print("2 ----")
print(f"key: {key.hex()}")
print(f"encrypted: {ciphertext.hex()}")
print(f"iv: {iv.hex()}")


# Stream cypher
# Chacha20

key = 'deb3d8eaee3ef609c4d736ea36c3c4385d0c4b99c46ac55556ba6ff513425218'
nonce = 'c7ca21647fd90c13'
cypher_text = '84157718cea30f137e9c47a4018ecc4c09cb8778094a92dc025588cb'

key = bytes.fromhex(key)
nonce = bytes.fromhex(nonce)
cypher_text = bytes.fromhex(cypher_text)

cipher = ChaCha20.new(key=key, nonce=nonce)
plaintext = cipher.decrypt(cypher_text)


print("3 ----")
print(f"plaintext: {plaintext}")
