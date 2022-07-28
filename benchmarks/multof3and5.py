
# CPython (default interpreter): 9.383s

# Pycom: 0.133s (70.5x faster)
# Pycom (--fastmath): 0.106s (88.5x faster)

# pypy: 0.495s (18.9x faster)

# Conclusion: 70-88x faster than CPython, 3.7-4.6x faster than pypy

total: int = 0
for i in range(1, 100000001):
    if i % 3 == 0 or i % 5 == 0:
        total += i
        
print(total)
