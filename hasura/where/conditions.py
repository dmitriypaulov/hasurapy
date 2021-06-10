from .condition import Condition, ComplexCondition

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

# {_and: {...conditions}}
class and_(ComplexCondition):
    def __init__(self, conditions):
        super().__init__("_and", conditions)

# {_or: {...conditions}}
class or_(ComplexCondition):
    def __init__(self, conditions):
        super().__init__("_or", conditions)

# {_not: {...conditions}}
class not_(ComplexCondition):
    def __init__(self, conditions):
        super().__init__("_not", conditions)