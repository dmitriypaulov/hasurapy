class limit():
    def __init__(self, value):
        self.value = value
    def __str__(self): return f"limit: {self.value}"

class offset():
    def __init__(self, value):
        self.value = value
    def __str__(self): return f"offset: {self.value}"

class page():
    def __init__(self, page, limit):
        self.page = page
        self.limit = limit
    def __str__(self): 
        return f"offset: {(self.page - 1) * self.limit}, limit: {self.limit}"