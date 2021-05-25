from collections import Mapping

def jsonify_value(value):
    if type(value) is bool: return str(value).lower()
    elif type(value) is str: return '"' + value + '"'
    return str(value)

class Where():
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __str__(self): 
        return self.stringify_parameter(
            "where", 
            *self.args, 
            **self.kwargs
        )

    def stringify_parameter(self, column, *args, **kwargs):
        conditions = []
        for col, val in kwargs.items():
            conditions.append(
                self.stringify_parameter(col, val)
            )
        conditions.extend(args)
        return f"{column}: {{{', '.join(conditions)}}}"

# pls, do not look down...
# Better look at this cat...
# 
#         /\_____/\
#        /  o   o  \
#       ( ==  ^  == )
#        )         (
#       (           )
#      ( (  )   (  ) )
#     (__(__)___(__)__)












# I warned you. Live with it.

not_like = lambda value: f"_nlike: {jsonify_value(value)}"
not_ilike = lambda value: f"_nilike: {jsonify_value(value)}"
like = lambda value: f"_like: {jsonify_value(value)}"
ilike = lambda value: f"_ilike: {jsonify_value(value)}"
similar = lambda value: f"_similar: {jsonify_value(value)}"
not_similar = lambda value: f"_nsimilar: {jsonify_value(value)}"

less_equal = lambda value: f"_lte: {jsonify_value(value)}"
greater_equal = lambda value: f"_gte: {jsonify_value(value)}"
less = lambda value: f"_lt: {jsonify_value(value)}"
greater = lambda value: f"_gt: {jsonify_value(value)}"
equal = lambda value: f"_eq: {jsonify_value(value)}"
not_equal = lambda value: f"_neq: {jsonify_value(value)}"
is_null = lambda value: f"_is_null: {jsonify_value(value)}"

in_ = lambda *args: f"_in: [{', '.join([jsonify_value(argument) for argument in args])}]"
not_in = lambda *args: f"_nin: [{', '.join([jsonify_value(argument) for argument in args])}]"

and_ = lambda **conditions: f"_and: {{{', '.join([column + ': {' + str(value) + '}' for column, value in conditions.items()])}}}"
or_ = lambda **conditions: f"_or: {{{', '.join([column + ': {' + str(value) + '}' for column, value in conditions.items()])}}}"
not_ = lambda **conditions: f"_not: {{{', '.join([column + ': {' + str(value) + '}' for column, value in conditions.items()])}}}"