implemented = [
    ('OP', 'LPAREN'),
    ('OP', 'RPAREN'),
    ('SIG', 'NEWLINE')
]

implementedtypes = [
    "STRING"
]

pythonbuiltins = [
    ('NAME', 'print')
]

cfuncs = [
    """
void print(const char *string){printf("%s", string);}
    
    """
]

class Compile:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.type = 0
        self.value = 1

        self.oktokens = self.checktokens()

    def iteratetokens(self):
        code = ""
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
                    if self.oktokens[i-1] != ("SIG", "NEWLINE"): code += ";"
                    else: code += "\n"

            if i + 1 == len(self.oktokens): code += ";"

        return code

            
    def checktokens(self):
        oktokens = []
        
        for token in self.tokens:
            if token not in implemented:
                if token[self.type] not in ["STRING", "NAME"]: continue

                elif token[self.type] == "NAME":
                    if token not in pythonbuiltins: continue
                    else: pass

                elif token[self.type] == "STRING": pass

            oktokens.append(token)

        return oktokens
