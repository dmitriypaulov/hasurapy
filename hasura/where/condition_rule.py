class ConditionRule():
    
    def __init__(self, column, condition):
        self.column = column
        self.condition = condition

    def __str__(self):
        if "__" in self.column: 
            string = ""
            blocks = self.column.split("__")
            for block in blocks: string += block + ": {"
            string += str(self.condition) + "}" * len(blocks)
            return string
        else: return f"{self.column}: {{{self.condition}}}"