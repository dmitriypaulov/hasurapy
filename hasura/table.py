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

    def select(self, *args, include = None, exclude = None, **kwargs):
        
        if not include: include = list(self.columns.values())
        else: 
            _include = []
            for column in include:
                if type(column) is str:
                    _column = self[column] 
                    if not _column: 
                        raise KeyError(
                           "Column %s doesn't exist in table %s" 
                           % (self.name, column)
                        )
                    _include.append(ColumnQuery(_column))
                elif type(column) is dict: _include.extend(ColumnQuery.from_dict(column))
                else: _include.append(ColumnQuery(column))
            include = _include

        # if not exclude: exclude = []
        # else: 
        #     _exclude = []
        #     for column in exclude:
        #         if type(column) is str:
        #             _column = self[column]
        #             if not _column: 
        #                 raise KeyError(
        #                     "Column %s doesn't exist in table %s" 
        #                     % (self.name, column)
        #                 )
        #             column = _column
        #         elif type(column) is dict:
        #             pass

        #         _exclude.append(column)
        #     exclude = _exclude
            
        

        # for column in exclude:
        #     if column in include:
        #         include.remove(column)

        _params = ""
        _fetch = " ".join([column_query.parse() for column_query in include])

        code = f"query{{{self.name}{_params}{{{_fetch}}}}}"
        return code

                
                

