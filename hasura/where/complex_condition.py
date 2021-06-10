from hasura.where import ConditionRule
from hasura.where.condition import Condition, equal, is_null

class ComplexCondition(Condition):
    
    def __init__(self, notation, *args, **kwargs):
        self.notation = notation
        self.rules = []
        
        for key, value in kwargs.items():
            if isinstance(value, Condition):
                self.rules.append(ConditionRule(key, value))

            if isinstance(value, (str, int, float, bool, list, dict)):
                self.rules.append(ConditionRule(key, equal(value)))

            if value == None: 
                self.rules.append(ConditionRule(key, is_null()))

        for arg in args:
            if isinstance(arg, ComplexCondition):
                self.rules.append(arg)

    def __str__(self): 
        _rules = ','.join(str(rule) for rule in self.rules)
        return f"{self.notation}: {{{_rules}}}"

# {_and: {...conditions}}
class and_(ComplexCondition):
    def __init__(self, *args, **kwargs):
        super().__init__("_and", *args, **kwargs)

# {_or: {...conditions}}
class or_(ComplexCondition):
    def __init__(self, *args, **kwargs):
        super().__init__("_or", *args, **kwargs)

# {_not: {...conditions}}
class not_(ComplexCondition):
    def __init__(self, *args, **kwargs):
        super().__init__("_not", *args, **kwargs)