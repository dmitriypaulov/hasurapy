from hasura.column import Column


class distinct_on():
    def __init__(self, column):
        if isinstance(column, Column):
            self.column = column.name
        else: self.column = column
        
    def __str__(self): return f"disinct_on: {self.column}"