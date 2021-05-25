asc = "asc"
desc = "desc"

class OrderBy():
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def stringify_parameter(self, column, value):

        if value in (asc, desc): return f"{column}: {value}"
        elif type(value) is list:
            items = []
            for item in value:
                if type(item) is tuple:
                    if len(item) == 2:
                        items.append(f"{item[0]}: {item[1]}")
                    else: raise ValueError("tuple representation of sorter must have 2 elements.")

                elif type(item) is str:
                    if item.startswith("-"): items.append(f"{item}: desc")
                    else: items.append(f"{item}: asc")
            return f"{column}: {{{', '.join(items)}}}"

    def __str__(self): 

        strings = []
        for column, value in self.kwargs.items():
            strings.append(self.stringify_parameter(column, value))
        return f"order_by: {{{', '.join(strings)}}}"