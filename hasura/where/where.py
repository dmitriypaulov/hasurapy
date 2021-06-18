from hasura.where.complex_condition import ComplexCondition
from hasura.where.condition_rule import ConditionRule
from hasura.where.condition import Condition, equal, is_null

class where():
    def __init__(self, *args, **kwargs):
        rules = []
        for key, value in kwargs.items():
            if isinstance(value, Condition): rules.append(ConditionRule(key, value))
            if isinstance(value, (str, int, float, bool, list, dict)): rules.append(ConditionRule(key, equal(value)))
            if value == None: rules.append(ConditionRule(key, is_null()))
        for arg in args:
            if isinstance(arg, ComplexCondition): 
                rules.append(arg)
        self.rules = rules

    def __str__(self): 
        if self.rules: return f"where: {{{', '.join(map(str, self.rules))}}}"
        return ""