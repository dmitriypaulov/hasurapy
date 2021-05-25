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

    def __fetch_columns(self):
        result = self.hasura.run_sql(f"""
            SELECT column_name FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = '{self.tablename}'
        """)

        columnnames = [column[0] for column in result["result"]]
        return columnnames[1:]

    def get(self, *args, one = False, count = False, total = False, page = None, limit = None, **kwargs):
        columns_to_fetch = []
        blocks_to_fetch = {}
        parameters = []
        
        if limit: parameters.append(f"limit: {limit}")
        if page and limit: parameters.append(f"offse0t: {(page - 1) * limit}")

        for arg in args:
            if isinstance(arg, str):
                columns_to_fetch.append(arg)
            else: parameters.append(str(arg))

        for key, value in kwargs.items():
            if isinstance(value, (list, tuple)):
                blocks_to_fetch[key] = value
            else: parameters.append(str(arg))

        _parameters = f"({','.join(parameters)})" if parameters else ""
        count_parameters = [item for item in parameters if item.split()[0] in ("where:", "distinct_on:")]
        _count_parameters = f"({','.join(count_parameters)})" if count_parameters else ""

        if not columns_to_fetch: columns_to_fetch.append("id")
        _columns_to_fetch = "\n".join(columns_to_fetch)

        _blocks_to_fetch = ""
        for key, value in blocks_to_fetch.items():
            _blocks_to_fetch += key + "{\n"
            for item in value: _blocks_to_fetch += f"\t{item}\n"
            _blocks_to_fetch += "}\n"

        count_code = f"""
                {self.tablename}_aggregate{'' if total else _count_parameters} {{
                    aggregate {{
                        count
                    }}
                }}
        """

        query_code = f"""
            query {{
                {self.tablename}{_parameters} {{
                    {_columns_to_fetch}
                    {_blocks_to_fetch}
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