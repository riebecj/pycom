import os
import time
import platform

if __name__ == "__main__":
    testdir = os.listdir("./tests/")
    for file in testdir:
        code = os.system(f"pycom -c tests/{file}") if platform.system() == "Linux" else os.system(f"pycom -c tests\\\\{file}")

    time.sleep(1.5)
    print("[INFO]: Tests complete. Check for any errors in the log.")