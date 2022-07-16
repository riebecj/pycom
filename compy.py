import sys
import tokenise
import compiler

try:
    filename = sys.argv[-1]

except IndexError:
    filename = "source.py"

flags = sys.argv[1:-1]

DEBUG = False

if "-d" in flags:
    DEBUG = True

if DEBUG:
    with open("test.txt", "w") as f: f.write("")
    with open("test.txt", "a+") as f:
        for i in tokenise.gettokens(filename):
            f.write(str(i) + "\n")
        exit(1)

print(compiler.Compile(tokenise.gettokens(filename)).iteratetokens())