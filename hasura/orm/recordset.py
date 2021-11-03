from hasura.conditions import where, is_in

UNTRACKED_NAMES = ["data", "table", "ids"]
class RecordSet():

    data = None
    table = None
    ids = None

    def __init__(self, data, table):
        self.data = data
        self.table = table
        self.ids = [row["id"] for row in data]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, name, default=False):
        for row in self.data:
            val = row.get(name, default)
            return val

    def __setitem__(self, name, value):
        self.write({name: value})

    def __getattr__(self, name, default=False):
        for row in self.data:
            val = row.get(name, default)
            return val

    def __setattr__(self, name, value):
        if name in UNTRACKED_NAMES:
            return super().__setattr__(name, value)
        self.write({name: value})

    def create(self, data):
        self.table.insert(_object=data)
        self.data.append(data)

    def write(self, data):
        self.data = self.table.update(
            where(id=is_in(self.ids)),
            _set=data,
        ).data

    def delete(self):
        self.table.delete(
            where(id=is_in(self.ids)))

    def filtered(self, func):
        res = []
        for row in self.data:
            if func(row):
                res.append(row)
        return RecordSet(res, self.table)

    def mapped(self, func):
        res = []
        for row in self.data:
            res.append(func(row))
        return RecordSet(res, self.table)
