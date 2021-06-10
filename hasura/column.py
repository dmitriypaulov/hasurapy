import textwrap

class Column():

    def __init__(self, name, _type, table, nested = None):

        self.name = name
        self._type = _type
        self.table = table
        self.nested = nested or {}

        for column in self.nested.values():
            column.parent = self

    def __setattr__(self, name, value): self.__dict__[name] = value
    def __getattr__(self, name, default = None): return self.__dict__.get(name, default)
    def __setitem__(self, name, value): self.__dict__[name] = value
    def __getitem__(self, name): return self.__dict__.get(name, None)
    def __call__(self, *args): return {self.name: [*args]}

    def __str__(self): return f"<Column name='{self.name}' type='{self._type}'>"
    def __repr__(self): return self.__str__()

    def pretty_str(self, show_nested = True):
        if self.nested and show_nested:
            _string = f"<Column name='{self.name}' type='{self._type}' nested = [\n"
            for column in self.nested.values():
                _string += textwrap.indent(
                    column.pretty_str(
                        show_nested = False
                    ), "\t"
                ) + "\n"
            _string += "]>"
            return _string
        else: return str(self)

class ColumnQuery():
    def __init__(self, column, *include):
        self.column = column
        self.fields = []

        if not include: self.fields = [ColumnQuery(column) for column in self.column.nested.values()]
        else:
            for field in include:
                
                if type(field) is str:
                    self.fields.append(ColumnQuery(self.column.nested[field]))
                
                elif type(field) is dict:
                    for key, value in field.items():
                        self.fields.append(ColumnQuery(self.column.nested[key], include = value))

    def __str__(self): 
        if self.fields: 
            return f"{self.column.name}: {{{' '.join(map(str, self.fields))}}}"
        else: return self.column.name