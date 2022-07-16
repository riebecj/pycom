implemented = [
    ('OP', 'LPAREN'),
    ('OP', 'RPAREN'),

    ('KW', 'def'),







    ('SIG', 'NEWLINE'),
    ('SIG', 'BLOCK_START'),
    ('SIG', 'BLOCK_END'),
    ('SIG', 'TYPEPOINTER'),
    ('SIG', 'COMMA')
]

implementedtypes = [
    "STRING"
]

pythonbuiltins = [
    ('NAME', 'print')
]

cfuncs = [
    'void print(std::string str){std::cout << str << std::endl;}'

]

types = ["str", "int", "float"]

pytypetoctype = {
    "str": "std::string",
    "int": "long long int",
    "float": "long double",
}

class Compile:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.type = 0
        self.value = 1

        self.oktokens = self.checktokens()

    def iteratetokens(self):
        code = "#include <iostream>\n#include <string>\n"
        for func in cfuncs: code += func + " "
        code += "\n"
        for i in range(len(self.oktokens)):
            if self.oktokens[i][self.type] == "NAME" or self.oktokens[i][self.type] == "FUNCREF" or self.oktokens[i][self.type] == "VARREF":
                code += self.oktokens[i][self.value]
            
            elif self.oktokens[i][self.type] == "OP":
                if self.oktokens[i][self.value] == "LPAREN":
                    code += "("

                elif self.oktokens[i][self.value] == "RPAREN":
                    code += ")"

            elif self.oktokens[i][self.type] == "STRING" or self.oktokens[i][self.type] == "INT":
                code += self.oktokens[i][self.value]

            elif self.oktokens[i][self.type] == "SIG":
                if self.oktokens[i][self.value] == "NEWLINE":
                    if self.oktokens[i-1] != ("SIG", "NEWLINE"): 
                        if self.oktokens[i-1][self.type] != "SIG" and not str(self.oktokens[i-1][self.value]).endswith(" TAB"):
                            code += ";"
                    else: code += "\n"

                elif self.oktokens[i] == ("SIG", "COMMA"):
                    code += ","

                elif self.oktokens[i] == ("SIG", "BLOCK_START"): code += "{"
                elif self.oktokens[i] == ("SIG", "BLOCK_END"): code += "}"

            elif self.oktokens[i][self.type] == "KW":
                if self.oktokens[i][self.value] == "def":
                    if self.oktokens[i+1] == ('FUNC', 'main'):
                        code += "int "

                    else:
                        code += "void "

            elif self.oktokens[i][self.type] == "FUNC":
                code += self.oktokens[i][self.value]

            elif self.oktokens[i][self.type] == "PARAM":
                if self.oktokens[i+1] == ("SIG", "TYPEPOINTER"):
                    if self.oktokens[i+2][1] in types:
                        typeofparam = self.oktokens[i+2][1] 
                    else: 
                        print(f"error: token #{i}: invalid type specified for param '{self.oktokens[i][self.value]}'")
                        exit(1)
                    ctypeofparam = pytypetoctype[typeofparam]
                    paramname = self.oktokens[i][self.value]
                    code += f"{ctypeofparam} {paramname}"


                else:
                    print(f"error: token #{i}: no type specified for param")
                    exit(1)

            if i + 1 != len(self.oktokens): 
                if self.oktokens[i+1] == ("SIG", "BLOCK_END"): code += ";"

        return code, self.oktokens

            
    def checktokens(self):
        oktokens = []
        
        for token in self.tokens:
            if token[self.type] == "SIG" and str(token[self.value]).endswith(" TAB"):
                oktokens.append(token)
                continue

            if token not in implemented:
                if token[self.type] not in ["STRING", "NAME", "FUNC", "VAR", "SIG", "PARAM", "TYPE", "INT", "VARREF", "FUNCREF"]: continue

                elif token[self.type] == "NAME":
                    if token not in pythonbuiltins: continue
                    else: pass
 
            oktokens.append(token)

        return oktokens
