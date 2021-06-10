import textwrap
from .column import Column, ColumnQuery

class Table():

    def __init__(self, name, hasura):
        
        self.name = name
        self.hasura = hasura
        self.fetch_metadata()

    def __setattr__(self, name, value): self.__dict__[name] = value
    def __getattr__(self, name, default = None): return self.__dict__.get(name, default)
    def __setitem__(self, name, value): self.__dict__[name] = value
    def __getitem__(self, name): return self.__dict__.get(name, None)

    def __str__(self): return f"<Table name='{self.name}' columns={list(self.columns.values())}>"
    def __repr__(self): return self.__str__()

    def pretty_str(self): 
        _string = f"<Table name='{self.name}' columns = [\n"
        for column in self.columns.values():
            _string += textwrap.indent(column.pretty_str(), "\t") + "\n"
        _string += "]>"
        return _string

    def fetch_metadata(self):
        
        result = self.hasura.query_request(
            _type = "run_sql",
            args = {
                "sql" :f"""
                SELECT column_name, data_type FROM information_schema.columns
                WHERE table_schema = 'public'
                AND table_name = '{self.name}';"""
            }
        )

        self.columns = {
            column[0]: Column(column[0], column[1], self)
            for column in result["result"][1:]
        }

        self.__dict__.update(self.columns)

    def _returning(self, include = None, exclude = None):

        column_queries = []
        if not include: column_queries = [ColumnQuery(column) for column in self.columns.values()]
        else: 
            for field in include:
                
                if type(field) is str:
                    column_queries.append(ColumnQuery(self.columns[field]))
                
                if type(field) is Column:
                    column_queries.append(ColumnQuery(self.columns[field.name]))
                
                elif type(field) is dict:
                    for key, value in field.items():
                        column_queries.append(ColumnQuery(self.columns[key], *value))

        if exclude:
            for field in exclude:
                
                if type(field) is str:
                    for index, query in enumerate(column_queries):
                        if query.column.name == field:
                            del column_queries[index]
                
                if type(field) is Column:
                    for index, query in enumerate(column_queries):
                        if query.column.name == field.name:
                            del column_queries[index]
                    
                if type(field) is dict:
                    for key, value in field.items():
                        for query in column_queries:
                            if query.column.name == key:
                                for exclude_column in value:
                                    for index, nested in enumerate(query.fields):
                                        if nested.column.name == exclude_column:
                                            del query.fields[index]

        return " ".join(map(str, column_queries))

    def select(self, *args, include = None, exclude = None, **kwargs):
        returning = self._returning(include, exclude)
        print(returning)

        
                
                

