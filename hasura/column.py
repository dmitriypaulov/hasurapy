import textwrap

class Column():

    def __init__(self, name, _type, table, columns = None):

        self.name = name
        self._type = _type
        self.table = table
        self.columns = columns or {}

        for column in self.columns.values():
            column.parent = self

    def __setattr__(self, name, value): self.__dict__[name] = value
    def __getattr__(self, name, default = None): return self.__dict__.get(name, default)
    def __setitem__(self, name, value): self.__dict__[name] = value
    def __getitem__(self, name): return self.__dict__.get(name, None)

    def __str__(self): return f"<Column name='{self.name}' type='{self._type}'>"
    def __repr__(self): return self.__str__()

    def pretty_str(self, show_nested = True):
        if self.columns and show_nested:
            _string = f"<Column name='{self.name}' type='{self._type}' columns = [\n"
            for column in self.columns.values():
                _string += textwrap.indent(
                    column.pretty_str(
                        show_nested = False
                    ), "\t"
                ) + "\n"
            _string += "]>"
            return _string
        else: return str(self)

class ColumnQuery():
    def __init__(self, column, include = None, exclude = None):
        self.column = column
        self.fields = []
        
        if not exclude: exclude = []

        _exclude = []
        for col in exclude:
           
            if type(col) is str:
                col = self.column[col]
           
            if type(col) is dict:
                pass

            _exclude.append(column) 
        
        self.exclude = _exclude

        if not include: include = list(self.columns.values())
        _include = []
        for column in include:
            if type(column) is str:
                column = self[column]
            _include.append(column)
        self.include = _include

        for column in include:
            if not column in exclude:
                self.fields.append(column.name)