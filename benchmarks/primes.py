# I am perfectly aware that this is a terrible algorithm for determining if a number is prime, this is just a 
# test for relative performance.

# CPython (default interpreter): 17.127s

# Pycom: 4.441s (3.85x faster)
# Pycom (with --fastmath): 3.994s (4.28x faster)

# pypy: 4.577s (3.74x faster)

# Conclusion: 3.85-4.28x faster than CPython, 1.03-1.14x faster than pypy

def is_prime(n):
    if n == 1:
        return 0
    for i in range(2, n):
        if n%i == 0:
            return 0

    return 1

def main():
    total = 0
    for i in range(1, 100001):
        total += is_prime(i)

    print(total)
