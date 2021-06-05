from _typeshed import NoneType

class Condition(): 

    def __init__(self, notation, value):
        self.notation = notation
        self.value = value

    def jsonify(self, value):
        if type(value) in (tuple, list): 
            _value = ','.join(
                list(
                    map(
                        self.jsonify, 
                        value
                    )
                )
            )
            return f"[{_value}]"
        elif type(value) is dict:
            _value = ','.join([
                key + ':' + self.jsonify(value) 
                for key, value in value.items()
            ])
            return f"{{{_value}}}"
        elif type(value) is bool: return str(value).lower()
        elif type(value) is NoneType: return "null"
        return value

    def __str__(self): return f"{self.notation}: {self.jsonify(self.value)}"

class ConditionRule():
    
    def __init__(self, column, condition):
        self.column = column
        self.condition = condition

    def __str__(self): return f"{self.column.name}: {{{self.condition}}}"

class ComplexCondition(Condition):
    
    def __init__(self, notation, rules):
        self.notation = notation
        self.rules = rules

    def __str__(self): 
        _rules = ','.join(str(rule) for rule in self.rules)
        return f"{self.notation}: {{{_rules}}}"