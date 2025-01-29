def solve(n, d, s):
    sol = 2

    # loop two times over the minimum value
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            # s[i] and s[j] will be the minimum values for the subset
            count = 2
            for k in range(n):
                if s[k] <= s[i] and s[k] <= s[j] or k == i or k == j:
                    continue
                elif abs(s[i] - s[k]) <= d or abs(s[j] - s[k]) <= d:
                    count += 1
            sol = max(sol, count)
    print(sol)


import sys
input = sys.stdin.readline

with open(sys.argv[1]) as f:
    t = int(f.readline())
    for _ in range(t):
        n, d = map(int, f.readline().split())
        s = list(map(int, f.readline().split()))
        solve(n, d, s)
