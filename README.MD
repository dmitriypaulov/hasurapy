# HasuraPy

---

Simple python wrapper for Hasura PostgreSQL graphql API.
Automatically grabs schema and metadata information to build models.

Usage example:

```python

from hasura import Hasura
from hasura.conditions import where, is_in
from hasura.order_by import order_by, desc

hasura = Hasura(
    "https://my.awesome.site/v1/graphql",
    headers = {
        "content-type": "application/json",
        "x-hasura-admin-secret": "<YOUR SECRET KEY>"
    }
)

cats = hasura.Cats
result = cats.select(
    order_by(livesLeft = desc), # desc(cats.livesLeft) or desc("livesLeft")
    where(
        color = is_in(
            "Grey",
            "Black",
            "Green(?)"
        )
    )
)

```

You can also use hasura's aggregation fields via using **aggregate** class.
For example:

```python
from hasura.aggregate import aggregate

cats = hasura.Cats.select(
    aggregate(
        count = True, min = "livesLeft",
        max = "hunger", average = "lifeLength"
    ),

    where(
        color = is_in(
            "Grey",
            "Black",
            "Transparent"
        )
    )
)
```

Also you can fetch on-fly paginated data by using **page** class.
For example:

```python
from hasura.pagination import page

cats = hasura.Cats.select(page(2, limit = 20))
```

Fetch exact fields you need by using **include** and **exclude** parameters of **select**. By default you will receive response with each column of the model.

```python
from hasura.pagination import page
from hasura.conditions import where, greater_then

cats = hasura.Cats.select(

    page(2, limit = 20)
    where(Owner__age = greater_then(18))

    include = [
        hasura.Cats.id,
        hasura.Cats.color,
        "name",
        "stringField",

        hasura.Cats.Owner(
            "age",
            "firstName",
            "lastName"
        )
    ]

)
```

That's all. Have fun and don't let your cats get hungry.
Yeah, I need to refactor some things. I'll do it after little break.