import sys
import tokenise
import compiler
import os, subprocess
from colorama import Fore
import time

def red(string): return Fore.RED + string + Fore.RESET

try: filename = sys.argv[-1]
except IndexError: filename = "source.py"

flags = sys.argv[1:-1]

DEBUG = False
INFO = False
RUN = False

if "-d" in flags: DEBUG = True
if "-i" in flags: INFO = True
if "-r" in flags: RUN = True

if DEBUG:
    with open("test.txt", "w") as f: f.write("")
    with open("test.txt", "a+") as f:
        for i in tokenise.gettokens(filename):
            f.write(str(i) + "\n")
        exit(1)

print(f"[INFO] Started compiling {filename};\n") if INFO else None

start_time = time.time()

compiledcode = compiler.Compile(tokenise.gettokens(filename)).iteratetokens()

cmd = f"echo '{compiledcode}' | gcc -w -xc - -o {filename.split('.')[0]}"

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

output, error = process.communicate()

end_time = time.time()

print(f"[INFO] Finished compiling '{filename}';\n") if INFO else None

if error != b"":
    print(red(f"error during conversion to c: {error}")) if INFO else None
    exit(1)

if output == b"":
    print(f"[INFO] Successfully compiled '{filename}' in {round(end_time-start_time, 2)}s ({round(end_time-start_time, 2) * 1000}ms)\n") if INFO else None