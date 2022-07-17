from keyword import kwlist
from typing import List

blockkw = ["if", "elif", "else", "for", "while", "try", "except", "finally", "def", "class", "with"]

def findnextkwline(lines: List[str], startind: int):
    for i in range(startind+1, len(lines)):
        if lines[i].split(" ")[0] in blockkw:
            return lines[i]


def refactorforcompiler(code: list):
    for index, line in enumerate(code):
        line = list(line)
        try:
            if line[-1] == "\n" and line[-2] != ":":
                line = line[:-1]

        except IndexError:
            continue

        line = "".join(line)

        code[index] = line

    while "\n" in code:
        code.remove("\n")

    lineandindlevel = []

    for line in code:
        indlevel = len(line) - len(str(line).lstrip()) if not str(line).isspace() or line != "\n" else 0
        lineandindlevel.append((line, indlevel))

    for i in range(len(lineandindlevel)):
        if i + 1 != len(lineandindlevel):
            if lineandindlevel[i][1] > lineandindlevel[i+1][1]:
                blocksdown = (lineandindlevel[i][1] - lineandindlevel[i+1][1]) // 4
                lineandindlevel[i] = (lineandindlevel[i][0] + (";" * blocksdown), lineandindlevel[i][1])

        if str(lineandindlevel[i][0]).strip().split(" ")[0] == "return" and str(lineandindlevel[i][0]).strip()[-1] != ";" and i + 1 <= len(lineandindlevel) and len(lineandindlevel) > 2:
            lineandindlevel[i] = (lineandindlevel[i][0] + ";", lineandindlevel[i][1])

    code = [line[0] for line in lineandindlevel]
    
    return "\n".join(code)