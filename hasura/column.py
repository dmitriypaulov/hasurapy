class Column():

    def __init__(self, name, _type, table):

        self.name = name
        self._type = _type
        self.table = table

    def __str__(self): return f"<Column name='{self.name}' type='{self._type}'>"
    def __repr__(self): return self.__str__()