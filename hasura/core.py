import requests
import textwrap
from .table import Table

class Hasura():

    def __init__(self, url, headers = None, query_url = None):

        self.url = url
        self.headers = headers or {}
        self.query_url = query_url or url.replace("graphql", "query")
        self.fetch_metadata()

    def __setattr__(self, name, value): self.__dict__[name] = value
    def __getattr__(self, name, default = None): return self.__dict__.get(name, default)
    def __setitem__(self, name, value): self.__dict__[name] = value
    def __getitem__(self, name): return self.__dict__.get(name, None)

    def __str__(self): return f"<Hasura url='{self.url}' tables={self.tables}>"
    def __repr__(self): return self.__str__()

    def pretty_str(self): 
        _string = f"<Hasura url='{self.url}' tables = [\n"
        for table in self.tables:
            _string += textwrap.indent(table.pretty_str(), "\t") + "\n"
        _string += "]"
        return _string

    def run_sql(self, sql):
        
        response = requests.post(
            self.query_url,
            headers = self.headers,
            json = {
                "type": "run_sql",
                "args": {"sql": sql + ";"}
            },
        )
        return response.json()

    def fetch_metadata(self):

        result = self.run_sql("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_type='BASE TABLE' 
            AND table_schema='public'
        """)

        self.tables = [
            Table(table[0], self)
            for table in result["result"][1:]
        ]
