#!/bin/env python3

import sys
import math
from collections import defaultdict
# Decomment here if you want to read to/write from file
# fin = open("input.txt", "r")  # Input file provided by the platform
# fout = open("output.txt", "w")  # Output file to submit

# Decomment here to read to/write from command line
fin = sys.stdin  # Input
fout = sys.stdout  # Output


# def count_intervals(N, a):
#     """
#     The function returns the number of distinct intervals (l, r) such that there exists a tuple (x, y, k)
#     where a[x] * a[y] = k^2 and a[l] <= min(x, y) < k^2 <= a[r].
#     """
#     a.sort()
#     print('a:', a)
#     # Create a list of all possible (i, j) pairs and their product
#     t = []
#     for i in range(N):
#         for j in range(i + 1, N):
#             product = a[i] * a[j]
#             # Check if the product is a perfect square
#             sqrt_product = int(math.isqrt(product))
#             if sqrt_product * sqrt_product == product:
#                 t.append((i, j, sqrt_product))  # Store indices instead of values
#     
#     print('t:', t)
#     # Now find all intervals (l, r) that contain at least one tuple
#     intervals = set()
#     for l in range(N):
#         for r in range(l + 1, N):
#             # Check if any tuple (i, j, k) fits within the interval (i, j)
#             for (x, y, k) in t:
#                 if a[l] == 1 and a[r] == 4:
#                     print(x, y, k)
#                 if a[l] <= min(a[x], a[y]) < k**2 <= a[r]:
#                     intervals.add((l, r))
#                     break  # No need to check further once we find a valid interval
#     
#     # Return the count of distinct intervals
#     print(sorted(intervals))
#     return len(intervals)

# def count_intervals(N, a):
#     """
#     The function returns the number of distinct intervals (l, r) such that 
#     within the interval there exists a tuple (i, j, k) of distinct indices
#     where a[i] * a[j] = a[k]^2
#     """
#     intervals = set()
#     
#     for l in range(N):
#         for r in range(l + 1, N):
#             for i in range(l, r + 1):
#                 for j in range(l, r + 1):
#                     for k in range(l, r + 1):
#                         if i != j and i != k and j != k:
#                             if a[i] * a[j] == a[k] * a[k]:
#                                 intervals.add((l, r))
#                                 break
#                     else:
#                         continue
#                     break
#                 else:
#                     continue
#                 break
#     
#     return len(intervals)
def count_intervals(N, a):
    """
    Optimized function to count intervals containing tuples (i,j,k) where a[i]*a[j] = a[k]^2
    Uses value-to-index mapping and pre-computation to improve performance
    """
    # Create value to indices mapping
    val_to_indices = defaultdict(list)
    for i, val in enumerate(a):
        val_to_indices[val].append(i)
    
    # Pre-compute squares up to max value in array
    max_val = max(a)
    squares = {i*i: i for i in range(1, int(max_val**0.5) + 1)}
    
    # Store valid tuples (i,j,k) grouped by their leftmost and rightmost indices
    interval_bounds = defaultdict(set)
    
    # For each possible k index and value
    for k, ak in enumerate(a):
        ak_squared = ak * ak
        
        # For each value that could be a[i]
        for val1, indices1 in val_to_indices.items():
            # If ak_squared / val1 exists in our array, it could be a[j]
            if ak_squared % val1 == 0:
                val2 = ak_squared // val1
                if val2 in val_to_indices:
                    # For each possible combination of i and j indices
                    for i in indices1:
                        for j in val_to_indices[val2]:
                            # Check if indices are distinct
                            if i != j and i != k and j != k:
                                # Store the leftmost and rightmost indices of the tuple
                                left = min(i, j, k)
                                right = max(i, j, k)
                                interval_bounds[left].add(right)
    
    # Count valid intervals using the interval bounds
    result = 0
    for l in range(N):
        # Find all intervals starting at l
        seen_rights = set()
        for left in range(l + 1):
            seen_rights.update(interval_bounds[left])
        
        # Count intervals [l,r] that contain at least one valid tuple
        for r in range(l + 1, N):
            if r in seen_rights:
                result += 1
    
    return result

T = int(fin.readline().strip())

for _ in range(T):
    N = int(fin.readline().strip())
    a = list(map(int, fin.readline().strip().split()))
    print(count_intervals(N, a))
