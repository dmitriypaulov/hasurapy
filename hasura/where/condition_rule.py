from hasura.where.condition import Condition, equal, is_null


class ConditionRule():
    
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition

    def __str__(self): return f"{self.name}: {{{self.condition}}}"
    def __repr__(self): return str(self)


class ConditionBlock():

    def __init__(self, name, rules = None): 
        self.name = name
        self.rules = rules or []

    def append(self, rule): self.rules.append(rule)
    def extend(self, rules): self.rules.extend(rules)

    def __str__(self): return f"{self.name}: {{{', '.join(map(str, self.rules))}}}"
    def __repr__(self): return str(self)