#!/bin/env python3

import sys

# Decomment here if you want to read to/write from file
# fin = open("input.txt", "r")  # Input file provided by the platform
# fout = open("output.txt", "w")  # Output file to submit

# Decomment here to read to/write from command line
fin = sys.stdin  # Input
fout = sys.stdout  # Output

def find_sum_of_times(N, M, t, f, emails):
    current_times = emails[:]
    
    for i in range(N):
        for j in range(M):
            if current_times[j] % t[i] != 0:
                current_times[j] += t[i] - (current_times[j] % t[i])
            current_times[j] += f[i]
    
    # Return the sum of all final times
    return sum(current_times)

# Read input
N, M = map(int, fin.readline().strip().split())
t = list(map(int, fin.readline().strip().split()))
f = list(map(int, fin.readline().strip().split()))
emails = list(map(int, fin.readline().strip().split()))

# Compute and print the result
fout.write(f"{find_sum_of_times(N, M, t, f, emails)}\n")
