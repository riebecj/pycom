def main():
    for i in range(1, 101):
        if i % 15 == 0:
            print("Fizzbuzz")
            continue

        elif i % 3 == 0:
            print("Fizz")
            continue

        elif i % 5 == 0:
            print("Buzz")
            continue

        print(i)
        
    return 0