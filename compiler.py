implemented = [
    ('OP', 'LPAREN'),
    ('OP', 'RPAREN'),

    ('KW', 'def'),







    ('SIG', 'NEWLINE'),
    ('SIG', 'BLOCK_START')
    
]

implementedtypes = [
    "STRING"
]

pythonbuiltins = [
    ('NAME', 'print')
]

cfuncs = [
    'void print(const char *string){printf("%s%c", string, 0x0A);}'

]

class Compile:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.type = 0
        self.value = 1

        self.oktokens = self.checktokens()

    def iteratetokens(self):
        code = ""
        for func in cfuncs: code += func + " "
        code += "\n"
        for i in range(len(self.oktokens)):
            if self.oktokens[i][self.type] == "NAME":
                if self.oktokens[i][self.value] == "print":
                    code += "print"
            
            elif self.oktokens[i][self.type] == "OP":
                if self.oktokens[i][self.value] == "LPAREN":
                    code += "("

                elif self.oktokens[i][self.value] == "RPAREN":
                    code += ")"

            elif self.oktokens[i][self.type] == "STRING":
                code += self.oktokens[i][self.value]

            elif self.oktokens[i][self.type] == "SIG":
                if self.oktokens[i][self.value] == "NEWLINE":
                    if self.oktokens[i-1] != ("SIG", "NEWLINE"): 
                        if self.oktokens[i-1][self.type] != "SIG" and not str(self.oktokens[i-1][self.value]).endswith(" TAB"):
                            code += ";"
                    else: code += "\n"

                elif self.oktokens[i][self.value] == "BLOCK_START": code += "{"

            elif self.oktokens[i][self.type] == "KW":
                if self.oktokens[i][self.value] == "def": 
                    code += "void "

            elif self.oktokens[i][self.type] == "FUNC":
                code += self.oktokens[i][self.value]

            if i + 1 == len(self.oktokens): code += ";}"

        return code

            
    def checktokens(self):
        oktokens = []
        
        for token in self.tokens:
            if token[self.type] == "SIG" and str(token[self.value]).endswith(" TAB"):
                oktokens.append(token)
                continue

            if token not in implemented:
                if token[self.type] not in ["STRING", "NAME", "FUNC", "VAR", "SIG"]: continue

                elif token[self.type] == "NAME":
                    if token not in pythonbuiltins: continue
                    else: pass

                elif token[self.type] == "FUNC" or token[self.type] == "VAR":
                    pass

                elif token[self.type] == "STRING": pass

            oktokens.append(token)

        return oktokens
