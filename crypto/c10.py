"""
    Cinese rest problem
x % 27 = 5
x % 2 = 0
x % 17 = 15
x % 61 = 22
x % 31 = 7
x % 1735938 = ?
"""
from sympy.ntheory.modular import crt
from math import prod

# Moduli and residues
modulos = [41, 74, 93, 97, 35]
residues = [25, 15, 1, 62, 15]

# Compute x using CRT
solution, mod = crt(modulos, residues)

print(f"x ≡ {solution} (mod {mod})")
print(solution % 957939990)  # Check modulo 1735938


# Compute the product of all moduli
N = prod(modulos)

# Compute the solution using the CRT formula
x = 0
for mod, res in zip(modulos, residues):
    Ni = N // mod
    Mi = pow(Ni, -1, mod)  # Modular inverse of Ni mod mod
    x += res * Ni * Mi

# Get the unique solution mod N
x = x % N

print(f"x ≡ {x} (mod {N})")
print(x % 957939990)  # Check modulo 1735938
