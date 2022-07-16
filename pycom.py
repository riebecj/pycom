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
RUNANDDEL = False
TOKENS = False
FAILPRINT = False

if "-d" in flags: DEBUG = True
if "-i" in flags: INFO = True
if "-r" in flags: RUN = True
if "-rd" in flags: RUNANDDEL = True
if "-t" in flags: TOKENS = True
if "-fp" in flags: FAILPRINT = True

if DEBUG:
    with open("test.txt", "w") as f: f.write("")
    with open("test.txt", "a+") as f:
        for i in tokenise.gettokens(filename):
            f.write(str(i) + "\n")
        exit(1)

print(f"[INFO] Started compiling {filename};\n") if INFO else None

start_time = time.time()

compiledcode, tokens = compiler.Compile(tokenise.gettokens(filename)).iteratetokens()

cmd = f"echo '{compiledcode}' | g++ -w -xc++ - -o {filename.split('.')[0]}"

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

output, error = process.communicate()

end_time = time.time()

print(f"[INFO] Finished compiling '{filename}';\n") if INFO else None

if TOKENS:
    print(tokens)
    exit(1)


if error != b"":
    print(red(f"error during conversion to c: {error.decode('utf-8')}"))
    print(compiledcode)
    exit(1)

if output == b"":
    print(f"[INFO] Successfully compiled '{filename}' in {round(end_time-start_time, 2)}s ({round(end_time-start_time, 2) * 1000}ms)\n") if INFO else None
    if RUNANDDEL:
        os.system(f"./{filename.split('.')[0]} && rm {filename.split('.')[0]}")

    elif RUN:
        os.system(f"./{filename.split('.')[0]}")