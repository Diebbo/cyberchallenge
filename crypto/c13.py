import sympy
import math


def genera_safe_prime(bit_length):
    """
    Genera una safe prime di almeno bit_length bit.

    Una safe prime è un numero primo p tale che (p-1)//2 è anch'esso primo.
    Tale secondo primo è chiamato "primo Sophie Germain".
    """
    while True:
        # Generiamo un numero primo candidato
        p = sympy.randprime(2**(bit_length-1), 2**bit_length)

        # Verifichiamo che (p-1)//2 sia primo
        sophie_germain = (p - 1) // 2

        if sympy.isprime(sophie_germain):
            return p, sophie_germain


# Generiamo una safe prime da almeno 1024 bit
bit_length = 1024
safe_prime, sophie_germain = genera_safe_prime(bit_length)

print(f"Safe Prime (lunghezza {safe_prime.bit_length()} bit): {safe_prime}")

# generatore
g = sympy.randprime(2, safe_prime - 1)

# Verifichiamo che g sia un generatore di Z_{safe_prime}
while pow(g, sophie_germain, safe_prime) == 1:
    g = sympy.randprime(2, safe_prime - 1)

print(f"Generatore: {g}")


# scelgo una chiave privata a caso
a = sympy.randprime(2, safe_prime - 1)
print(f"Chiave privata: {a}")

# calcolo la chiave pubblica
A = pow(g, a, safe_prime)

print(f"Chiave pubblica: {A}")
