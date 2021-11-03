from typing import Iterable
from hasura.column import Column


class aggregate():
    def __init__(self, count = None, min = None, max = None, sum = None, average = None, all = False):
        self.count = count
        self.min = min
        self.max = max
        self.sum = sum
        self.all = all
        self.average = average

        self.tablename = None
        self.parameters = None

    def compile_metric(self, metric, notation):
        result = notation + "{"
        if isinstance(metric, str): return result + metric + "}"
        elif isinstance(metric, Column): return result + metric.name + "}"
        elif isinstance(metric, Iterable):
            cols = []
            for col in metric:
                if isinstance(col, str): cols.append(col)
                elif isinstance(col, Column): cols.append(col.name)
            return result + " ".join(cols) + "}"

    def __str__(self):
        metrics = []
        if self.count: metrics.append("count")
        if self.min: metrics.append(self.compile_metric(self.min, "min"))
        if self.max: metrics.append(self.compile_metric(self.max, "max"))
        if self.sum: metrics.append(self.compile_metric(self.sum, "sum"))
        if self.average: metrics.append(self.compile_metric(self.average, "avg"))
        metrics = " ".join(metrics)

        return f"{self.tablename}_aggregate{self.parameters}{{aggregate{{{metrics}}}}}"
