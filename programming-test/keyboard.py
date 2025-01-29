#!/bin/env python3

import sys

# Decomment here if you want to read to/write from file
# fin = open("input.txt", "r")  # Input file provided by the platform
# fout = open("output.txt", "w")  # Output file to submit

# Decomment here to read to/write from command line
fin = sys.stdin  # Input
fout = sys.stdout  # Output


def find_key(L, s):
    # Create a set of all lowercase letters
    all_letters = set('abcdefghijklmnopqrstuvwxyz')
    # Find the missing letter
    missing_letter = all_letters - set(s)
    # Return the missing letter
    return missing_letter.pop()

N = int(fin.readline().strip())

for _ in range(N):
    L = int(fin.readline().strip())
    s = fin.readline().strip()
    print(find_key(L, s), file=fout)
