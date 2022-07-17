import tokenize
import sys

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
	";": "BLOCK_END"
}

keywords = ["import", "if", "elif", "else", "for", "while", "try", "except", "finally", "True", "False", "continue",
"break", "pass", "as", "assert", "def", "class", "await", "return", "from", "async", "await", "del", "global",
"lambda", "nonlocal", "raise", "with", "yield"]

blockkw = ["if", "elif", "else", "for", "while", "try", "except", "finally", "def", "class", "with"]

operators = ["+", "-", "*", "/", "//", "%", "**", "+=", "-=", "*=", "/=", "%=", "**=", "//=", "&=", "|=", ">>=", "<<=", "=",
    "==", "!=", ">", "<", ">=", "<=", "&", "|", "^", ">>", "<<", "(", ")", "[", "]", "{", "}", "and", "or", "in", "is", "not"]

signifiers = [":", ";", ".", ",", "\n", "\t"]

types = ["str", "int", "float", "list", "dict", "set"]

varnames = []

funcnames = []

importnames = []

classnames = []

def isfloat(token: str):
	token = str(token)
	sides = token.split(".")

	if len(sides) == 2:
		side1, side2 = sides[0], sides[1]

		if side1.isdigit() and side2.isdigit(): return True

		else: return False

	else: return False

	
def wordtotoktype(word: str):
	if word in keywords: return "KW"
	elif word in operators: return "OP"
	elif word in signifiers or word.startswith("    "): return "SIG"
	elif word[0] == '"' or word[0] == 'f' and word[-1] == '"': return "STRING"
	elif word.isdigit(): return "INT"
	elif isfloat(word): return "FLOAT"
	else: return "NAME"


def printtokens(tokens: list):
	for token in tokens: print(token, end="\n")

def allcharacterssame(s):
    n = len(s)
    for i in range(1, n):
        if s[i] != s[0]:
            return False
 
    return True

def gettokens(filename: str):
	try:
		with open(filename, "rb") as f:
			tokens = tokenize.tokenize(f.readline)
			token_list = [t.string for t in tokens][1:-2]
			while "" in token_list: token_list.remove("")
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
				for i in range(len(token_list)):
					if token_list[i] == ("KW", "def"):
						token_list[i+1] = ("FUNC", token_list[i+1][1])
						funcnames.append(token_list[i+1][1])

					elif token_list[i][0] == ("KW", "class"):
						token_list[i+1] = ("CLASS", token_list[i+1][1])
						classnames.append(token_list[i+1][1])

					elif token_list[i] == ("KW", "import"):
						token_list[i+1] = ("IMPORT_MODULE", token_list[i+1][1])
						importnames.append(token_list[i+1][1])

					elif token_list[i] == ("SIG", "BLOCK_START"):
						if token_list[i+1][1] in ["str", "int", "float", "list", "dict", "set"]:
							token_list[i] = ("SIG", "TYPEPOINTER")

					elif token_list[i][0] == "NAME":
						if token_list[i][1] in types:
							token_list[i] = ("TYPE", token_list[i][1])

						elif token_list[i+1] == ("OP", "ASSIGN"):
							token_list[i] = ("VAR", token_list[i][1])
							varnames.append(token_list[i][1])
						
						elif token_list[i-1] == ("KW", "for"):
							token_list[i] = ("VAR", token_list[i][1])
							varnames.append(token_list[i][1])

						elif token_list[i+1] == ("SIG", "BLOCK_START"):
							token_list[i] = ("PARAM", token_list[i][1])
							varnames.append(token_list[i][1])

						elif token_list[i-1] == ("SIG", "DOT"):
							token_list[i] = ("METHOD", token_list[i][1])

						else:
							if token_list[i][1] in varnames: token_list[i] = ("VARREF", token_list[i][1])
							elif token_list[i][1] in funcnames: token_list[i] = ("FUNCREF", token_list[i][1])
							elif token_list[i][1] in importnames: token_list[i] = ("IMPORTREF", token_list[i][1])
							elif token_list[i][1] in classnames: token_list[i] = ("CLASSREF", token_list[i][1])
			
			except IndexError:
				return token_list


			return token_list

	except FileNotFoundError:
		print(f"tokenise.py: error: '{filename}' not found", file=sys.stderr)
		exit(1)
