from hasura.column import Column

class direction():
    def __init__(self, notation, column):
        self.notation = notation
        if isinstance(column, Column): self.name = column.resolve()
        elif isinstance(column, str): self.name = column
        else: raise TypeError(f"column type should be <hasura.column.Column> or <str>")

    def __str__(self): return f"{self.name}: {self.notation}"
    def __repr__(self): return str(self)

class asc(direction):
    def __init__(self, column):
        super().__init__("asc", column)

class desc(direction):
    def __init__(self, column):
        super().__init__("desc", column)

class SortingBlock():
    def __init__(self, name, rules = None): 
        self.name = name
        self.rules = rules or []

    def append(self, rule): self.rules.append(rule)
    def extend(self, rules): self.rules.extend(rules)

    def __str__(self): return f"{self.name}: {{{', '.join(map(str, self.rules))}}}"
    def __repr__(self): return str(self)

class order_by():
    def __init__(self, *args, **kwargs):
        self.rules = []

        for arg in args: 
            if isinstance(arg, direction): 
                self.rules.append(arg)

        for key, value in kwargs.items():
            if value in (asc, desc): self.rules.append(value(key))

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
                    block = SortingBlock(blockname)
                    blocks.append(block)

                rule.name = restname
                block.append(rule)
                delete.append(rule)
                
        for rule in delete: rules.remove(rule)
        for block in blocks: self.build_blocks(block.rules)
        rules.extend(blocks)

    def __str__(self): return f"order_by: {{{', '.join(map(str, self.rules))}}}"

        