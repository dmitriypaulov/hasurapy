import requests

class Hasura():

    def __init__(self, url, headers = None, query_url = None):
        
        self.url = url
        self.headers = headers or {}
        self.query_url = query_url or url.replace("graphql", "query")  
        self.build_schema()

    def __setattr__(self, name, value): self.__dict__[name] = value
    def __getattr__(self, name, default): return self.__dict__.get(name, default)

    def build_schema(self):
        
        tablenames = self.__fetch_tablenames()
        for tablename in tablenames:
            table = Table(tablename, self)
            table.build_columns()
            setattr(self, tablename, table)

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

    def request_graphql(self, query = None, mutation = None):
        if not query and not mutation: return
        if query: _json = {"query": query}
        elif mutation: _json = {"mutation": mutation}
        response = requests.post(
            self.url,
            headers = self.headers,
            json = _json
        ) 
        return response.json()
            
    def __fetch_tablenames(self):
        
        result = self.run_sql("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_type='BASE TABLE' 
            AND table_schema='public'
        """)

        tablenames = [table[0] for table in result["result"]]
        return tablenames[1:]

class Table():

    def __init__(self, tablename, hasura):
        
        self.tablename = tablename
        self.hasura = hasura
        self.columns = []

    def build_columns(self):
        self.columns = self.__fetch_columns()

    def stringify_block(self, key, value):
        code = f"{key}: {{"
        for column in value:
            code += f"\n{column}"
        code += "}"
        return code

    def __fetch_columns(self):
        result = self.hasura.run_sql(f"""
            SELECT column_name FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = '{self.tablename}'
        """)

        columnnames = [column[0] for column in result["result"]]
        return columnnames[1:]

    def get(self, *args, one = False, count = False, total = False, page = None, limit = None, **kwargs):

        columns = []
        blocks = {}
        params = []
        
        if limit: params.append(f"limit: {limit}")
        if page and limit: params.append(f"offset: {(page - 1) * limit}")

        for arg in args:
            if isinstance(arg, str):
                columns.append(arg)
            else: params.append(str(arg))
        columns = "\n".join(columns) if columns else "\nid"

        for key, value in kwargs.items():
            if isinstance(value, (list, tuple)):
                blocks[key] = value
            else: params.append(str(arg))

        blocks = "\n".join([
            self.stringify_block(key, value)
            for key, value 
            in blocks.items()
        ])
        
        cparams = list(filter(lambda item: item.startswith("where") or item.startswith("distinct_on"), params))
        cparams = f"({', '.join(cparams)})" if cparams else ""
        params = f"({', '.join(params)})" if params else ""

        count_code = f"""
            {self.tablename}_aggregate{'' if total else cparams} {{
                aggregate {{
                    count
                }}
            }}
        """

        query_code = f"""
            query {{
                {self.tablename}{params} {{
                    {columns}
                    {blocks}
                }}
                {count_code if count else ''}
            }}
        """
        
        response = self.hasura.request_graphql(query = query_code)

        try:
            result = {"data": response["data"][self.tablename]}
            if one and result["data"]: result["data"] = result["data"][0]
            if count: result["count"] = response["data"][self.tablename + "_aggregate"]["aggregate"]["count"]
            return result
        except KeyError: raise(f"Failed to get rows from hasura endpoint: {response}")
        

    


















"""

organization = bot.Organizations.get(where(organizationId = 12))
user = bot.Users.set(where(id = 1), langId = 2, one = True)
new_user = bot.Users.add(langId = 1)
languages = bot.Langs.get(count = True)
categories = bot.CategoriesList.get(page = 3, limit = 20)

bot.Employees.get(
    "id",
    "userId",
    User = [
        "firstname",
        "lastname
    ]
)

"""