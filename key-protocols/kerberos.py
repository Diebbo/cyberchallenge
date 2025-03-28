import json
from datetime import datetime
from Crypto.Cipher import AES
import base64

# Session key (K_A_TGS)
session_key = '465927'  # Adjust to proper length for encryption

# Create the Authenticator
authenticator = {
    "client_name": "Alice",
    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}
print("Authenticator:", authenticator)
authenticator_bytes = json.dumps(authenticator).encode('utf-8')

# Encrypt the Authenticator (using AES for example)


def encrypt_message(message, key):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX)
    encrypted_message, tag = cipher.encrypt_and_digest(message)
    return encrypted_message


# encrypted_authenticator = encrypt_message(authenticator_bytes, session_key)

# Base64 encode the encrypted Authenticator for transmission
# encrypted_authenticator_b64 = base64.b64encode(
    # encrypted_authenticator).decode('utf-8')

# Send the Authentication Ticket and the encrypted Authenticator to the TGS
print("Authentication Ticket:",
      "NC82dGRia083UVQvd1pTRkNhUzU5cGZHVTZHTEkwMXBkYlpDSWRZRUc2ZWVGejM0U3JaTElqZkp5N252SWZQVHpYeENoc2o5OGJETVVnMlBVM3Zwa2c9PQ==")
# print("Encrypted Authenticator (Base64):", encrypted_authenticator_b64)
