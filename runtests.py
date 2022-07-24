import os

if __name__ == "__main__":
    testdir = os.listdir("./tests/")
    for file in testdir:
        os.system(f"./pycom.py -c tests/{file}")

    print("[INFO]: Tests complete. Check for any errors in the log.")