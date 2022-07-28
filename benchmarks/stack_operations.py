
# CPython (default interpreter): 8.857s

# Pycom: 2.132s (4.15x faster)
# Pycom (with --fastmath): 1.992s (4.44x faster)

# pypy: 3.113s (2.84x faster)

# Conclusion: 4.15-4.44x faster than CPython, 1.45-1.56x faster than pypy

def main():
    stack = []

    for i in range(1, 15000001):
        if i * 3 % 56 == 43:
            print(i)
        stack.append(69)
        stack.pop()
