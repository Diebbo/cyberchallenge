"""
    RSA encryption and decryption using RSA-CRT
"""
from Crypto.Util.number import inverse
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes


def rsa_crt_decrypt(ciphertext, p, q, d):
    """
    Perform RSA decryption using the Chinese Remainder Theorem (CRT).

    Args:
        ciphertext (int): The ciphertext to decrypt.
        p (int): The first prime factor of the modulus.
        q (int): The second prime factor of the modulus.
        d (int): The private exponent.

    Returns:
        int: The decrypted plaintext as an integer.
    """
    # Compute the modulus
    n = p * q

    # Compute dp and dq
    dp = d % (p - 1)
    dq = d % (q - 1)

    # Compute the modular inverses
    q_inv = inverse(q, p)

    # Compute the partial results
    m1 = pow(ciphertext, dp, p)
    m2 = pow(ciphertext, dq, q)

    # Combine the results using CRT
    h = (q_inv * (m1 - m2)) % p
    plaintext = (m2 + h * q) % n

    return plaintext


# Example usage
if __name__ == "__main__":
    # Example RSA parameters (use secure values in practice)
    key = RSA.generate(2048)
    p = key.p
    q = key.q
    e = key.e
    d = key.d
    n = key.n

    m = b"Hello, RSA!"

    print(f"Original plaintext: {m}\nprime factors: {
          p}, {q}\nprivate exponent: {d}")

    # Encrypt the plaintext
    ciphertext = pow(bytes_to_long(m), e, n)
    print("Encrypted ciphertext:", ciphertext)

    plaintext = rsa_crt_decrypt(ciphertext, p, q, d)
    print("Decrypted plaintext:", long_to_bytes(plaintext))
