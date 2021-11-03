import os
import json
import requests
import textwrap
from pathlib import Path
from .table import Table
from .column import Column

class Hasura():

    def __init__(self, url, headers = None, query_url = None, force_fetch = False):

        self.url = url
        self.headers = headers or {}
        self.query_url = query_url or url.replace("graphql", "query")
        metadata_load = self.load_metadata()
        if not metadata_load or force_fetch:
            self.fetch_metadata()
            self.save_metadata()

    def __setattr__(self, name, value): self.__dict__[name] = value
    def __getattr__(self, name, default = None) -> Table: return self.__dict__.get(name, default)
    def __setitem__(self, name, value): self.__dict__[name] = value
    def __getitem__(self, name) -> Table: return self.__dict__.get(name, None)

    def __str__(self): return f"<Hasura url='{self.url}' tables={list(self.tables.values())}>"
    def __repr__(self): return self.__str__()

    def pretty_str(self):
        _string = f"<Hasura url='{self.url}' tables = [\n"
        for table in self.tables.values():
            _string += textwrap.indent(table.pretty_str(), "\t") + "\n"
        _string += "]>"
        return _string

    def query_request(self, _type, args = None):

        response = requests.post(
            self.query_url,
            headers = self.headers,
            json = {
                "type": _type,
                "args": args or {}
            },
        )
        return response.json()

    def graphql_request(self, code, _type = "query"):

        response = requests.post(
            self.url,
            headers = self.headers,
            json = {_type: code},
        )
        return response.json()

    def save_metadata(self):
        data = {
            "tables": [self.tables[table].to_json()
                    for table in self.tables]
        }
        with open(Path(os.getcwd()) / "metadata.json", "w+", encoding="utf-8") as f:
            json.dump(data, f, separators=(',', ':'), ensure_ascii=False)

    def load_metadata(self):
        try:
            with open(Path(os.getcwd()) / "metadata.json",  encoding="utf-8") as f:
                data = json.load(f)
                self.tables = {}
                for table in data["tables"]:
                    self.tables[table["name"]] = Table.from_json(table, self)
                self.__dict__.update(self.tables)
            return True
        except Exception: pass

    def fetch_metadata(self):

        result = self.query_request(
            _type = "run_sql",
            args = {
                "sql": """
                SELECT table_name FROM information_schema.tables
                WHERE table_type='BASE TABLE'
                AND table_schema='public';"""
            }
        )

        self.tables = {
            table[0]: Table(table[0], self)
            for table in result["result"][1:]
        }

        self.__dict__.update(self.tables)
        metadata = self.query_request("export_metadata")
        for source in metadata["sources"]:
            for table in source.get("tables", []):

                tablename = table["table"]["name"]
                _table = self[tablename]

                many2one_relationships = table.get("object_relationships", [])
                many2many_relationships = table.get("array_relationships", [])
                for rel in many2one_relationships: rel["type"] = "many2one"
                for rel in many2many_relationships: rel["type"] = "many2many"

                for relationship in (*many2one_relationships, *many2many_relationships):

                    ref_table = None
                    ref_column = relationship["using"].get("foreign_key_constraint_on", None)
                    if type(ref_column) is dict: ref_table = ref_column["table"]["name"]
                    if not ref_table: ref_table = self.query_request(
                        _type = "run_sql",
                        args = {
                            "sql": f"""
                            SELECT ccu.table_name AS foreign_table_name FROM information_schema.table_constraints AS tc 
                            JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name 
                            AND tc.table_schema = kcu.table_schema JOIN information_schema.constraint_column_usage 
                            AS ccu ON ccu.constraint_name = tc.constraint_name AND ccu.table_schema = tc.table_schema
                            WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name='{tablename}' AND kcu.column_name='{ref_column}';
                            """
                        }
                    )

                    if type(ref_table) is dict:
                        result = ref_table["result"]
                        if len(result) > 1: ref_table = result[1][0]
                        else: continue

                    col = Column(
                        relationship["name"],
                        relationship["type"],
                        _table,
                        self[ref_table].columns
                    )

                    _table.columns[relationship["name"]] = col
                    _table[relationship["name"]] = col
