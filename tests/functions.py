def is_prime(n):
    if n == 1:
        return 0
    for i in range(2, n):
        if n%i == 0:
            return 0

    return 1

def main():
    total = 0
    for i in range(1, 101):
        total += is_prime(i)

    print(total)