import os
import time

if __name__ == "__main__":
    testdir = os.listdir("./tests/")
    for file in testdir:
        os.system(f"./pycom.py -c tests/{file}")

    time.sleep(1.5)
    print("[INFO]: Tests complete. Check for any errors in the log.")