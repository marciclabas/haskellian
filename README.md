# Haskellian

> The python functional programming library you need

```bash
pip install haskellian
```

## Why
- Lazy imports + stub files -> great linting and 0 import time (thanks to [`lazy-loader`](https://github.com/scientific-python/lazy_loader))
- Monadic, method chaining style
- Great typing and overloads


#### `Iter[A]` (generators made ergonomic)

```python
from haskellian import Iter

Iter(range(100000000000)) \
  .map(lambda x: 2*x) \
  .filter(lambda x: x % 2 == 0) \
  .batch(2) \
  .skip(1)
  #.sync() # don't recommend it...

# Iter([(4, 6), (8, 10), (12, 14), (16, 18), (20, 22), ...])
```

#### `Promise[A]` (awaitables made ergonomic)

```python
from haskellian import Promise, promise as P

async def fetch_users() -> list[str]:
  ...
async def fetch_user(id) -> str:
  ...

await Promise(fetch_users()) \
  .bind(lambda ids: P.all(map(fetch_user, ids))) \
  .then(sorted)
```

#### `Either[L, R]`

##### Method-chaining style

```python
from haskellian import Either, Left, Right, either as E

def fetch_users() -> Either[str, list[str]]:
  ...

def fetch_user(id: str) -> Either[str, dict]:
  ...

def parse_user(user: dict) -> Either[str, User]:
  ...

def print_one():
  fetch_users() \
    .bind(lambda ids: fetch_user(ids[0])) \
    .bind(parse_user) \
    .fmap(print)
```

##### Do-notation style

```python
@E.do()
def print_one():
  users = fetch_users().unsafe()
  raw_user = fetch_user(users[0]).unsafe()
  user = parse_user(raw_user).unsafe()
  print(user)
```

> Explanation: `.unsafe()` raises an `IsLeft` exception; `@E.do()` simply wraps the function in a `try...except IsLeft` block, returning the raised `Left` if so.

#### `AsynIter[A]` 

```python
from haskellian import AsynIter, asyn_iter as AI

@AI.lift
async def gen():
  for i in range(10):
    yield i

await gen().map(lambda x: 2*x).filter(lambda x: x % 2 == 0).batch(2).skip(1).sync()
```

### `Dict[A]`

```python
from haskellian import Dict

Dict({'a': 1, 'b': 2}) \
  .filter(lambda v: v % 2 == 0) \
  .map(lambda v: 2*v) \

# Dict({'b': 4})
```