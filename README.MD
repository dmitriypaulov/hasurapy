# HasuraPy

---

Simple python wrapper for Hasura PostgreSQL graphql API. 
Automatically grabs schema and metadata information to build models.

Usage example:

```python

from hasura import Hasura
from hasura.where import Where, in_
from hasura.order_by import OrderBy, desc

hasura = Hasura(
    "https://my.awesome.site/v1/graphql",
    headers = {
        "content-type": "application/json",
        "x-hasura-admin-secret": "<YOUR SECRET KEY>"
    }
)

cats = hasura.Cats.select(
    OrderBy(livesLeft = desc),
    Where(
        color = in_(
            "Grey", 
            "Black", 
            "Green(?)"
        )
    )
)

```

You can also use hasura's aggregation fields via using **count** and **total** parameters for **select** method of model.
For example:

```python

cats = hasura.Cats.select(
    count = True,
    Where(
        color = in_(
            "Grey", 
            "Black", 
            "Transparent"
        )
    )
)
# cats = {"data": [...], "count": 3}

hungry_cats = hasura.Cats.select(
    count = True,
    total = True,
    Where(isHungry = equal(True))
)
# cats = {"data": [...], "count": *Total count of Cats rows*}

```

Also you can fetch on-fly paginated data by passing **page** and **limit** parameters.
For example:

```python

cats = hasura.Cats.select(
    page = 4,
    limit = 20,
    count = True,
    total = True
)

```

That's all. Have fun and don't let your cats get hungry.
Yeah, I need to refactor some things. I'll do it after little break.