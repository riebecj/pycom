import os

try:
    os.remove("source")

except FileNotFoundError:
    print("works")