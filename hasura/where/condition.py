class Condition(): 

    def __init__(self, notation, value):
        self.notation = notation
        self.value = value

    def jsonify(self, value):
        if type(value) in (tuple, list): 
            _value = ', '.join(
                list(
                    map(
                        self.jsonify, 
                        value
                    )
                )
            )
            return f"[{_value}]"
        elif type(value) is dict:
            _value = ', '.join([
                key + ':' + self.jsonify(value) 
                for key, value in value.items()
            ])
            return f"{{{_value}}}"
        elif type(value) is bool: return str(value).lower()
        elif type(value) is str: return f'"{value}"'
        elif value == None: return "null"
        return value

    def __str__(self): return f"{self.notation}: {self.jsonify(self.value)}"

# {_eq: "value"}
class equal(Condition):
    def __init__(self, value):
        super().__init__("_eq", value)

# {_neq: "value"}
class not_equal(Condition):
    def __init__(self, value):
        super().__init__("_neq", value)

# {_lt: "value"}
class less_then(Condition):
    def __init__(self, value):
        super().__init__("_lt", value)

# {_gt: "value"}
class greater_then(Condition):
    def __init__(self, value):
        super().__init__("_gt", value)

# {_lte: "value"}
class less_or_equal(Condition):
    def __init__(self, value):
        super().__init__("_lte", value)

# {_gte: "value"}
class greater_or_equal(Condition):
    def __init__(self, value):
        super().__init__("_gte", value)

# {_is_null: false}
class is_null(Condition):
    def __init__(self, value = True):
        super().__init__("_is_null", value)

# {_in: [1, 2, 3]}
class is_in(Condition):
    def __init__(self, value = None):
        if not value: value = []
        super().__init__("_in", value)

# {_nin: [1, 2, 3]}
class not_in(Condition):
    def __init__(self, value = None):
        if not value: value = []
        super().__init__("_nin", value)

# {_like: "value"}
class like(Condition):
    def __init__(self, value):
        super().__init__("_like", value)

# {_ilike: "value"}
class insensitive_like(Condition):
    def __init__(self, value):
        super().__init__("_ilike", value)

# {_nlike: "value"}
class not_like(Condition):
    def __init__(self, value):
        super().__init__("_nlike", value)

# {_nilike: "value"}
class not_insensitive_like(Condition):
    def __init__(self, value):
        super().__init__("_nilike", value)

# {_similar: "value"}
class similar(Condition):
    def __init__(self, value):
        super().__init__("_similar", value)

# {_nsimilar: "value"}
class not_similar(Condition):
    def __init__(self, value):
        super().__init__("_nsimilar", value)


