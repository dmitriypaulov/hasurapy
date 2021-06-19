from hasura.where.complex_condition import ComplexCondition
from hasura.where.condition_rule import ConditionBlock, ConditionRule
from hasura.where.condition import Condition, equal, is_null

class where():
    def __init__(self, *args, **kwargs):
        self.rules = []
        for key, value in kwargs.items():
            rule = self.parse_rule(key, value)
            if rule: self.rules.append(rule)
            
        for arg in args:
            if isinstance(arg, ComplexCondition): 
                self.rules.append(arg)

        self.build_blocks(self.rules)

    def build_blocks(self, rules):
        blocks = []
        delete = []
        for rule in rules:
            if "__" in rule.name:
                splitted = rule.name.split("__", maxsplit = 1)
                blockname = splitted[0]
                restname = splitted[1]
                
                exists = list(filter(lambda x: x.name == blockname, blocks))
                if exists: block = exists[0]
                else: 
                    block = ConditionBlock(blockname)
                    blocks.append(block)
                block.append(ConditionRule(restname, rule.condition))
                delete.append(rule)
                
        for rule in delete: rules.remove(rule)
        for block in blocks: self.build_blocks(block.rules)
        rules.extend(blocks)

    def parse_rule(self, key, value):
        if isinstance(value, Condition): return ConditionRule(key, value)
        if isinstance(value, (str, int, float, bool, list, dict)):  return ConditionRule(key, equal(value))
        if value == None: return ConditionRule(key, is_null())

    def __str__(self): 
        if self.rules: return f"where: {{{', '.join(map(str, self.rules))}}}"
        return ""