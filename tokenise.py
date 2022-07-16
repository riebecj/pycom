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
	":": "BLOCK_START"
}

keywords = ["import", "if", "elif", "else", "for", "while", "try", "except", "finally", "True", "False", "continue",
"break", "pass", "as", "assert", "def", "class", "await", "return", "from", "async", "await", "del", "global",
"lambda", "nonlocal", "raise", "with", "yield"]

operators = ["+", "-", "*", "/", "//", "**", "+=", "-=", "*=", "/=", "%=", "**=", "//=", "&=", "|=", ">>=", "<<=", "=",
    "==", "!=", ">", "<", ">=", "<=", "&", "|", "^", ">>", "<<", "(", ")", "[", "]", "{", "}", "and", "or", "in", "is", "not"]

signifiers = [":", ".", ",", "\n", "\t"]

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
					if token_list[i][0] == "SIG" and token_list[i][1].isspace():
						token_list[i] = (typeofcurrent, f"{int(len(current) / 4)} TAB")

			for i in range(len(token_list)):
				if token_list[i][0] == "KW" and token_list[i][1] == "def":
					token_list[i+1] = ("FUNC", token_list[i+1][1])
					funcnames.append(token_list[i+1][1])

				elif token_list[i][0] == "KW" and token_list[i][1] == "class":
					token_list[i+1] = ("CLASS", token_list[i+1][1])
					classnames.append(token_list[i+1][1])

				elif token_list[i][0] == "KW" and token_list[i][1] == "import":
					token_list[i+1] = ("IMPORT_MODULE", token_list[i+1][1])
					importnames.append(token_list[i+1][1])

				elif token_list[i][0] == "NAME":
					if token_list[i+1][0] == "OP" and token_list[i+1][1] == "ASSIGN":
						token_list[i] = ("VAR", token_list[i][1])
						varnames.append(token_list[i][1])

					elif token_list[i-1][0] == "OP" and token_list[i-1][1] == "LPAREN" and token_list[i-2][0] == "FUNC":
						token_list[i] = ("VAR", token_list[i][1])
						varnames.append(token_list[i][1])

					elif token_list[i+1][0] == "SIG" and token_list[i+1][1] == "COMMA":
						token_list[i] = ("VAR", token_list[i][1])
						varnames.append(token_list[i][1])

					elif token_list[i+1][0] == "OP" and token_list[i+1][1] == "RPAREN":
						token_list[i] = ("VAR", token_list[i][1])
						varnames.append(token_list[i][1])

					elif token_list[i-1][0] == "SIG" and token_list[i-1][1] == "DOT":
						token_list[i] = ("METHOD", token_list[i][1])

					else:
						if token_list[i][1] in varnames: token_list[i] = ("VARREF", token_list[i][1])
						elif token_list[i][1] in funcnames: token_list[i] = ("FUNCREF", token_list[i][1])
						elif token_list[i][1] in importnames: token_list[i] = ("IMPORTREF", token_list[i][1])
						elif token_list[i][1] in classnames: token_list[i] = ("CLASSREF", token_list[i][1])

			return token_list

	except FileNotFoundError:
		print(f"tokenise.py: error: '{filename}' not found", file=sys.stderr)
		exit(1)