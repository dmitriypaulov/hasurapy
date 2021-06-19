class InsertObject():

    def __init__(self, data):
        self.data = data

    def jsonify(self, data): 
        _data = []
        for key, value in data.items():
            if type(value) in (tuple, list): 
                _value = ', '.join(
                    list(
                        map(
                            self.jsonify, 
                            value
                        )
                    )
                )
                value = f"[{_value}]"
            elif type(value) is dict:
                _value = ', '.join([
                    key + ':' + self.jsonify(value) 
                    for key, value in value.items()
                ])
                value = f"{{{_value}}}"
            elif type(value) is bool: value = str(value).lower()
            elif type(value) is str: value = f'"{value}"'
            elif value == None: value = "null"
            _data.append(f"{key}: {value}")
        return ", ".join(_data)

    def __str__(self): return f"object: {{{self.jsonify(self.data)}}}"
    def __repr__(self): return str(self)

class UpdateObject(InsertObject):
    def __str__(self): return f"_set: {{{self.jsonify(self.data)}}}"