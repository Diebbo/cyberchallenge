import string
import re
from statistics import mean
from pwn import *

# Connect to the remote service
s = remote('benchmark.challs.cyberchallenge.it', 9031)
s.recvline_contains(b"password")

# Define character set to try
CHARSET = string.ascii_letters + string.digits + string.punctuation

# Already known part of the password
known_password = "CCIT{"
password = known_password


def try_password(s, password):

    # Send password
    s.sendline(password.encode())

    # Receive response
    response = s.recvline_startswith(b"Give").decode()

    # Extract clock cycles using regex
    match = re.search(r'checked in (\d+) clock cycles', response)
    if match:
        cycles = int(match.group(1))
        correct = "Correct" in response
        return cycles, correct
    elif "Correct" in response:
        return -1, True
    else:
        return 0, False

# Function to find the next character


def find_next_char(password):
    max_cycles = 0
    next_char = None
    results = []

    for c in CHARSET:
        test_password = password + c
        try:
            cycles, correct = try_password(s, test_password)
            results.append((c, cycles, correct))

            # Check if we found the correct character
            if correct:
                return c, True

            # Keep track of character with highest cycle count
            if cycles > max_cycles:
                max_cycles = cycles
                next_char = c

            print(f"Tried: {test_password}, Cycles: {
                  cycles}, Correct: {correct}")

        except Exception as e:
            print(f"Error with {test_password}: {e}")

    # Sort and print the top 5 candidates for debugging
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    print("\nTop 5 candidates:")
    for c, cycles, correct in sorted_results[:5]:
        print(f"Character: {c}, Cycles: {cycles}, Correct: {correct}")

    return next_char, False


# Main loop to find the complete flag
print(f"Starting with known prefix: {password}")
found_complete_flag = False

try:
    # Try to find remaining characters
    while not found_complete_flag and "}" not in password[len(known_password):]:
        next_char, is_correct = find_next_char(password)

        if next_char:
            password += next_char
            print(f"Current password: {password}")

            if is_correct:
                found_complete_flag = True
                print(f"FOUND CORRECT FLAG: {password}")
                break
        else:
            print("Failed to find next character. Something went wrong.")
            break

    # If we reached here without finding the complete flag
    # but we already have a closing brace, consider it done
    if "}" in password[len(known_password):] and not found_complete_flag:
        print(f"Found closing brace. Final password: {password}")

finally:
    # Close the connection
    s.close()
    print(f"Final result: {password}")
