import tokenize
import sys
import refactor
import os
import re
import time

tokmap = {
    "\n": "NEWLINE",
    "\t": "TAB",

    "+": "PLUS",
    "-": "SUB",
    "*": "MULT",
    "/": "DIV",
    "//": "FLOORDIV",
    "%": "MOD",
    "**": "POW",
    "&": "BITAND",
    "|": "BITOR",
    "^": "BITXOR",
    "~": "BITFLIP",
    "<<": "BITLSHIFT",
    ">>": "BITRSHIFT",
    "+=": "PLUSAND",
    "-=": "SUBAND",
    "*=": "MULTAND",
    "/=": "DIVAND",
    "//=": "FLOORDIVAND",
    "%=": "MODAND",
    "**=": "POWAND",
    "&=": "BITANDAND",
    "|=": "BITORAND",
    "^=": "BITXORAND",
    "~=": "BITFLIPAND",
    "<<=": "BITLSHIFTAND",
    ">>=": "BITRSHIFTAND",
    "(": "LPAREN",
    ")": "RPAREN",
    "[": "LSPAREN",
    "]": "RSPAREN",
    "{": "LCPAREN",
    "}": "RCPAREN",
    "=": "ASSIGN",
    "==": "EQUAL",
    "!=": "NOTEQUAL",
    ">": "GREATER",
    "<": "LESS",
    ">=": "GREATEROREQUAL",
    "<=": "LESSOREQUAL",

    ".": "DOT",
    ",": "COMMA",
    ":": "BLOCK_START",
    "->": "FUNCTYPEPOINTER",
    ";": "BLOCK_END"
}

keywords = ["import", "if", "elif", "else", "for", "while", "match", "case", "try", "except", "finally", "True", "False", "continue",
            "break", "pass", "as", "assert", "def", "class", "await", "return", "from", "async", "await", "del", "global",
            "lambda", "nonlocal", "raise", "with", "yield"]

blockkw = ["if", "elif", "else", "for", "while", "try",
           "except", "finally", "def", "class", "with", "match", ]

operators = ["+", "-", "*", "/", "//", "%", "**", "+=", "-=", "*=", "/=", "%=", "**=", "//=", "&=", "|=", ">>=", "<<=", "=",
             "==", "!=", ">", "<", ">=", "<=", "&", "|", "^", ">>", "<<", "(", ")", "[", "]", "{", "}", "and", "or", "in", "is", "not"]

signifiers = [":", ";", ".", ",", "\n", "\t", "->"]

types = ["str", "int", "float", "list", "dict", "set", "bool"]

pylistmethodtocpp = {
    "append": "push_back",
    "pop": "pop_back"
}

varnames = []

funcnames = []

importnames = []

classnames = []


def fstringtocppformat(stringtok: str):

    if "{" not in stringtok or "}" not in stringtok:
        return stringtok[1:]

    stringtok = stringtok[1:]

    formatargs = []

    for i in range(len(stringtok)):
        if stringtok[i] == '{':
            wi = i + 1
            expr = ""
            while stringtok[wi] != "}":
                expr += stringtok[wi]
                wi += 1

            formatargs.append(expr)

    strformatargs = ", " + ", ".join(formatargs)

    return "fmt::format(" + re.sub("\{.*?\}", "{}", stringtok) + strformatargs + ")"


def isfloat(token: str):
    token = str(token)
    sides = token.split(".")

    if len(sides) == 2:
        side1, side2 = sides[0], sides[1]

        if side1.isdigit() and side2.isdigit():
            return True

        else:
            return False

    else:
        return False


def wordtotoktype(word: str):
    try:
        if word in keywords:
            return "KW"
        elif word in operators:
            return "OP"
        elif word in signifiers or word.startswith("    "):
            return "SIG"
        elif word[0] == '"' or word[0] == 'f' and word[-1] == '"':
            return "STRING" if word[0] != 'f' else "FSTRING"
        elif word.isdigit():
            return "INT"
        elif isfloat(word):
            return "FLOAT"
        else:
            return "NAME"

    except AttributeError:
        return


def printtokens(tokens: list):
    for token in tokens:
        print(token, end="\n")


def allcharacterssame(s):
    n = len(s)
    for i in range(1, n):
        if s[i] != s[0]:
            return False

    return True


def gettokens(filename: str, flags: list):

    print(
        f"[VINFO] Started tokenisation of {filename};\n") if "-v" in flags else None

    start_time = time.perf_counter()

    try:
        with open(filename, "r") as src:
            source = src.readlines()
        with open("temp.py", "x") as x:
            pass
        with open("temp.py", "w") as temp:
            temp.write(refactor.refactorforcompiler(source))
        with open("temp.py", "rb") as f:
            tokens = tokenize.tokenize(f.readline)
            token_list = [t.string for t in tokens][1:-2]

        os.remove("temp.py")

        while "" in token_list:
            token_list.remove("")

        for i in range(len(token_list)):
            current = token_list[i]
            typeofcurrent = wordtotoktype(current)

            try:
                token_list[i] = (typeofcurrent, tokmap[current])

            except KeyError:
                token_list[i] = (typeofcurrent, current)
                if token_list[i][0] == "SIG" and token_list[i][1].startswith("    ") and allcharacterssame(token_list[i][1]):
                    token_list[i] = ("SIG", f"{int(len(current) / 4)} TAB")

            try:
                if token_list[i] == ("KW", "def"):
                    funcnames.append(token_list[i+1][1])

                elif token_list[i] == ("KW", "class"):
                    classnames.append(token_list[i+1][1])

                elif token_list[i] == ("KW", "import"):
                    importnames.append(token_list[i+1][1])

                elif token_list[i] == ("SIG", "BLOCK_START"):
                    if i + 1 != len(token_list):
                        if token_list[i+1][1] in ["str", "int", "float", "list", "dict", "set", "bool"]:
                            token_list[i] = ("SIG", "TYPEPOINTER")

                elif token_list[i][0] == "FSTRING":
                    token_list[i] = (
                        "STRING", fstringtocppformat(token_list[i][1]))

                elif token_list[i] == ("OP", "LSPAREN"):
                    token_list[i] = ("OP", "LCPAREN")

                elif token_list[i] == ("OP", "RSPAREN"):
                    token_list[i] = ("OP", "RCPAREN")

                elif token_list[i][0] == "NAME":
                    if token_list[i][1] in types:
                        if token_list[i+1] != ("OP", "LPAREN"):
                            token_list[i] = (
                                "TYPE", token_list[i][1])

                    elif token_list[i+1] == ("OP", "ASSIGN"):
                        token_list[i] = ("VAR", token_list[i][1])
                        varnames.append(token_list[i][1])

                    elif token_list[i+1] == ("SIG", "BLOCK_START") and token_list[i+2][1] in types and token_list[i+3] == ("OP", "ASSIGN"):
                        token_list[i] = ("VAR", token_list[i][1])
                        varnames.append(token_list[i][1])

                    elif token_list[i-1] == ("KW", "for"):
                        token_list[i] = ("VAR", token_list[i][1])
                        varnames.append(token_list[i][1])

                    elif token_list[i+1] == ("SIG", "BLOCK_START"):
                        token_list[i] = ("PARAM", token_list[i][1])
                        varnames.append(token_list[i][1])

                    elif token_list[i-1] == ("SIG", "DOT"):
                        if token_list[i][1] not in pylistmethodtocpp:
                            token_list[i] = ("METHOD", token_list[i][1])

                        else:
                            token_list[i] = ("METHOD", pylistmethodtocpp[token_list[i][1]])

                    elif token_list[i-1] == ("KW", "import"):
                        token_list[i] = ("IMPORT_MODULE", token_list[i][1])

                    elif token_list[i-1] == ("KW", "def"):
                        token_list[i] = ("FUNC", token_list[i][1])

                    elif token_list[i-1] == ("KW", "class"):
                        token_list[i] = ("CLASS", token_list[i][1])

                    else:
                        if token_list[i][1] in varnames:
                            token_list[i] = (
                                "VARREF", token_list[i][1])
                        elif token_list[i][1] in funcnames:
                            token_list[i] = (
                                "FUNCREF", token_list[i][1])
                        elif token_list[i][1] in importnames:
                            token_list[i] = (
                                "IMPORTREF", token_list[i][1])
                        elif token_list[i][1] in classnames:
                            token_list[i] = (
                                "CLASSREF", token_list[i][1])

            except IndexError:

                continue

                end_time = time.perf_counter()
                print(
                    f"[VINFO] Successfully tokenised {filename} in {round(end_time-start_time, 3)}s ({round(end_time-start_time, 3) * 1000}ms);\n") if "-v" in flags else None

                return token_list

        for i in range(len(token_list)):
            if i + 1 != len(token_list):
                if token_list[i] == ("SIG", "BLOCK_START"):
                    if token_list[i+1][1] in ["str", "int", "float", "list", "dict", "set"]:
                        token_list[i] = ("SIG", "TYPEPOINTER")

        end_time = time.perf_counter()
        print(
            f"[VINFO] Successfully tokenised {filename} in {round(end_time-start_time, 3)}s ({round(end_time-start_time, 3) * 1000}ms);\n") if "-v" in flags else None

        return token_list

    except FileNotFoundError:
        print(f"tokenise.py: error: '{filename}' not found", file=sys.stderr)
        os.remove("temp.py")
        exit(1)
