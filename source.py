import os

try:
    os.remove("d")

except FileNotFoundError:
    print("caught")