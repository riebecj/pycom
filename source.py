import math

def main():
    total: int = 0
    for i in range(1, 1001):
        if i % 3 == 0 or i % 5 == 0:
            total += i
        
    print(total)

    return 0