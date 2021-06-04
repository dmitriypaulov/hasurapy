import textwrap
from .column import Column

class Table():

    def __init__(self, name, hasura):
        
        self.name = name
        self.hasura = hasura
        self.fetch_metadata()

    def __setattr__(self, name, value): self.__dict__[name] = value
    def __getattr__(self, name, default = None): return self.__dict__.get(name, default)
    def __setitem__(self, name, value): self.__dict__[name] = value
    def __getitem__(self, name): return self.__dict__.get(name, None)

    def __str__(self): return f"<Table name='{self.name}' columns={self.columns}>"
    def __repr__(self): return self.__str__()

    def pretty_str(self): 
        _string = f"<Table name='{self.name}' columns = [\n"
        for column in self.columns:
            _string += textwrap.indent(str(column), "\t") + "\n"
        _string += "]"
        return _string

    def fetch_metadata(self):
        
        result = self.hasura.run_sql(f"""
            SELECT column_name, data_type FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = '{self.name}'
        """)

        self.columns = [
            Column(column[0], column[1], self)
            for column in result["result"][1:]
        ]

