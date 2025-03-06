# generate a password of 16bytes
import Crypto.Random.random as run

p1 = ''
s1 = 'a91b8bb91d90eed967dea620329c566e881cf329d6f25e2671a065b3c759e6dd'

p2 = 'a'
s2 = '0abd70fb548b89592c73b15456d1e78cf8329315e92eadd592a2d629de9ccda322b33bd00864d5af0841d066e7826b76'


"""
BLOCK = 16

def pad(s):
  return s + (BLOCK - len(s) % BLOCK) * chr(BLOCK - len(s) % BLOCK)

def randkey():
  return "".join([printable[randint(0, len(printable)-8)] for _ in range(BLOCK)]).encode()


cipher = AES.new(randkey(), AES.MODE_ECB)

password = input("Give me the password to encrypt:")
password = pad(password + FLAG).encode()
password = hexlify(cipher.encrypt(password)).decode()
print("Here is you secure encrypted password:", password)
    """

# The code above is a simple encryption algorithm that encrypts a password with a random key and a flag. given the input give 'a' * 16 and the oupt i need to find the flag.
# The code is using AES in ECB mode, the key is generated with the randkey() function and the password is padded with the pad() function.
# The password is then encrypted with the key and the flag and the result is returned as a hex string.

# i can get the password by receiving the encrypted password for 'a' * i with i from 1 to 16.
