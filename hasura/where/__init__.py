class ConditionRule():
    
    def __init__(self, column, condition):
        self.column = column
        self.condition = condition

    def __str__(self): return f"{self.column}: {{{self.condition}}}"
