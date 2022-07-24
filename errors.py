class Error:
    def __init__(self, errortype, errormsg):
        self.errortype = errortype
        self.errormsg = errormsg
    
    def returnerror(self):
        return f"pycom: {self.errortype}: {self.errormsg}"


def cpperrortopycomerror(error: str):
    newerrorlines = []
    errorlines = [line.strip() for line in error.split("\n") if not line.startswith("<stdin>: ")]
    while "" in errorlines:
        errorlines.remove("")
    errorlines = [line.split("error: ", 1)[1] for line in errorlines if not line == ""]

    for error in errorlines:
        if error.endswith(" was not declared in this scope"):
            errortype = "NameError"
            errortok = error.removesuffix("’ was not declared in this scope")[1:]
            errormsg = f"name '{errortok}' is not defined"
            newerrorlines.append("    " + Error(errortype, errormsg).returnerror())

        else:
            newerrorlines.append("    " + error)
    
    return "\n".join(newerrorlines)