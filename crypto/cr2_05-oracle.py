from Crypto.Util.number import long_to_bytes
import sys

sys.set_int_max_str_digits(1000000)  # Increase limit if necessary

# Given encrypted flag
flag_encrypted = 26206750254688960615165873421685959381276407836858941390061691871618921615652000639231451913467496911529261042026928854735723490544434518727849939959718116510702715862492728486056176981603055218468182271022200775540368920712982228115574209227017924817001633034641174934679088175234629272535708672179280941481  # Replace with actual value
# possible values of e
e = 65547
# Step 1: Multiply ciphertext by 2^e (without needing n)
factor = 2
c_prime = flag_encrypted * (factor ** e)

print("Send this ciphertext for decryption:", c_prime)

# Step 2: Get decrypted message from the server
m_prime = int(input("Paste the decrypted message from the oracle: "))  # Get from the CTF server

# Step 3: Flag should be roughly half of m_prime
print("Possible flag values:")
print(long_to_bytes(m_prime // 2))
print(long_to_bytes((m_prime - 1) // 2))  # Handle rounding issues
print(long_to_bytes((m_prime + 1) // 2))
