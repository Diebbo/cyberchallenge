#!/bin/env python3

import sys

# Uncomment for testing via command line
fin = sys.stdin  # Input
fout = sys.stdout  # Output

def solve_alien_operations(n, operations):
    # Define the alphabet and prepare helpers for rotation and swaps
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    alpha_len = len(alphabet)
    char_to_idx = {char: i for i, char in enumerate(alphabet)}  # Map char to index
    idx_to_char = {i: char for i, char in enumerate(alphabet)}  # Map index to char

    # Initialize state variables
    result = []  # The resulting string as a list for efficient appends/deletes
    swap_map = {char: char for char in alphabet}  # Tracks current swaps
    net_rotation = 0  # Tracks net rotation
    state_matrix = []  # Tracks the state of the string after each `add` operation

    # Helper to apply the current transformations (swap + rotation) to a character
    def translate_char(c):
        # Apply swap map
        c = swap_map[c]
        # Apply rotation
        new_idx = (char_to_idx[c] + net_rotation) % alpha_len
        return idx_to_char[new_idx]

    # Process each operation
    for op in operations:
        parts = op.split()
        command = parts[0]

        if command == "add":
            # Add character after translation
            char = parts[1]
            translated_char = translate_char(char)
            result.append(translated_char)
            # Save the current state to the state matrix
            state_matrix.append("".join(result))

        elif command == "del":
            # Remove the last character if present
            if result:
                result.pop()

        elif command == "swap":
            # Update the swap map and modify the current result string
            a, b = parts[1], parts[2]
            # Update the swap_map
            for key, val in list(swap_map.items()):
                if val == a:
                    swap_map[key] = b
                elif val == b:
                    swap_map[key] = a
            # Apply swap to all characters in the result
            result = [b if c == a else a if c == b else c for c in result]

        elif command == "rot":
            # Update net rotation (accumulated lazily)
            net_rotation += int(parts[1])

    # Debug: Print the state matrix (optional, remove for production)
    for i, state in enumerate(state_matrix):
        print(f"State {i+1}: {state}", file=sys.stderr)

    # Return the final string
    return "".join(result)


# Read input and execute
N = int(fin.readline().strip())
operations = [fin.readline().strip() for _ in range(N)]

# Output the result
fout.write(solve_alien_operations(N, operations) + "\n")
