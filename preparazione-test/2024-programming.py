#!/bin/python3

labels = {}
variables = {}

with open('input.txt', 'r') as f:
    N = int(f.readline().strip())  # Initialize N
    l = 1  # line i'm reading

    lines = f.readlines()  # Read all lines at once

    while l <= N:
        # Process each line
        line = lines[l - 1].strip()
        print("reading", line)

        if line.startswith('add'):
            var, num = line.split()[1:]
            num = int(num)
            variables[var] = variables.get(var, 0) + num
        elif line.startswith('sub'):
            var, num = line.split()[1:]
            num = int(num)
            variables[var] = variables.get(var, 0) - num
        elif line.startswith('mul'):
            var, num = line.split()[1:]
            num = int(num)
            variables[var] = variables.get(var, 0) * num
        elif line.startswith('lab'):
            name = line.split()[1]
            labels[name] = l
        elif line.startswith('jmp'):
            var, num, name = line.split()[1:]
            num = int(num)
            if variables.get(var, 0) == num:
                # jump to label
                l = labels[name]

        l += 1

sum = 0
for k, v in variables.items():
    print(f'{k} {v}')
    sum += v
print(sum)
