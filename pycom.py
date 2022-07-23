#!/usr/bin/env python3.10

import sys
import tokenise
import compiler
import os
import subprocess
from colorama import Fore
import time


def red(string): return Fore.RED + string + Fore.RESET


try:
    filename = sys.argv[-1]
except IndexError:
    filename = "source.py"

flags = sys.argv[1:-1]

DEBUG = False
INFO = False
RUN = False
RUNANDDEL = False
TOKENS = False
RAWTOKENS = False
FAILPRINT = False
PRINT = False
OUTPUT = False
FASTMATH = False
VERBOSE = False
TEST = False
CHECK = False

if "-d" in flags or "--debug" in flags:
    DEBUG = True
if "-i" in flags or "--info" in flags:
    INFO = True
if "-v" in flags or "--verbose" in flags:
    VERBOSE = True
    INFO = True
if "-r" in flags or "--run" in flags:
    RUN = True
if "-rd" in flags or "--runanddelete" in flags:
    RUNANDDEL = True
if "-t" in flags or "--tokens" in flags:
    TOKENS = True
if "-rt" in flags or "--rawtokens" in flags:
    RAWTOKENS = True
if "-fp" in flags or "--failprint" in flags:
    FAILPRINT = True
if "-p" in flags or "--print" in flags:
    PRINT = True
if "-o" in flags or "--output" in flags:
    OUTPUT = True
if "-fm" in flags or "--fastmath" in flags:
    FASTMATH = True
if "-c" in flags or "--check" in flags:
    CHECK = True

if RAWTOKENS:
    print(tokenise.gettokens(filename, flags))
    exit()


print(f"\n[INFO] Started compiling {filename};\n") if INFO else None

start_time = time.perf_counter()

compiledcode, tokens = compiler.Compile(tokenise.gettokens(
    filename, flags), flags, filename).iteratetokens()

if DEBUG:
    with open("tests/test.txt", "w") as f:
        f.write("")
    with open("tests/test.txt", "a+") as f:
        for i in tokens:
            f.write(str(i) + "\n")
        exit(1)

if TOKENS:
    print(tokens)
    exit(1)

if PRINT:
    print(compiledcode)
    exit(1)

if OUTPUT:
    try:
        outputname = sys.argv[sys.argv.index("-o") + 1]

    except Exception:
        outputname = sys.argv[sys.argv.index("--output") + 1]

else:
    outputname = None

if FASTMATH:
    if outputname is None:
        cmd = f"echo '{compiledcode}' | g++ -std=c++20 -O3 -w -xc++ - -o {filename.split('.')[0]}"
    else:
        cmd = f"echo '{compiledcode}' | g++ -std=c++20 -O3 -w -xc++ - -o {outputname}"

else:
    if outputname is None:
        cmd = f"echo '{compiledcode}' | g++ -std=c++20 -O2 -w -xc++ - -o {filename.split('.')[0]}"
    else:
        cmd = f"echo '{compiledcode}' | g++ -std=c++20 -O2 -w -xc++ - -o {outputname}"

process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, shell=True)

output, error = process.communicate()

end_time = time.perf_counter()

print(f"[INFO] Finished compiling '{filename}';\n") if INFO else None

if error != b"":
    print(red(f"error: compilation error: {error.decode('utf-8')}"))
    print(compiledcode) if FAILPRINT else None
    exit(1)

if output == b"":
    print(f"[INFO] Successfully compiled '{filename}' in {round(end_time-start_time, 2)}s ({round(end_time-start_time, 2) * 1000}ms)\n") if INFO else None
    if RUNANDDEL:
        os.system(f"./{filename.split('.')[0]} && rm {filename.split('.')[0]}")

    elif RUN:
        os.system(f"./{filename.split('.')[0]}")
