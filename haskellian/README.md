# Haskellian

> The python functional programming library you need

```bash
pip install haskellian
```

## Goals
- 0 import time
- Monadic, method chaining style
- Great typing and overloads


## Classes

#### `Iter[A]`

```python
from haskellian import Iter, iter as I

@I.lift
def gen():
  for i in range(100000000000):
    yield i

gen() \
  .map(lambda x: 2*x) \
  .filter(lambda x: x % 2 == 0) \
  .batch(2) \
  .skip(1)
  #.sync() # don't recommend it...

# Iter([(4, 6), (8, 10), (12, 14), (16, 18), (20, 22), ...])
```

#### `Either[L, R]`

```python
from haskellian import Either, either as E

def fetch_users() -> Either[str, list[str]]:
  ...

def fetch_user(id: str) -> Either[str, dict]:
  ...

def parse_user(user: dict) -> Either[str, User]:
  ...

@E.do()
def print_one():
  users = fetch_users().unsafe()
  raw_user = fetch_user(users[0]).unsafe()
  user = parse_user(raw_user).unsafe()
  print(user)
```

Explanation:
- `.unsafe()` raises unwraps the value or raises an `IsLeft` exception
- `@E.do()` wraps the function in a `try...except IsLeft` block, returning the possibly raised `Left`

#### `Dict[A]`

```python
from haskellian import Dict

Dict({ 'a': 1, 'b': 2, 'c': 4 }) \
  .filter_v(lambda v: v % 2 == 0) \
  .evolve({ 'c': lambda x: -x })
  .map_v(lambda v: 2*v)

# Dict({ 'b': 4, 'c': -8 })
```

#### `AsynIter[A]` 

```python
from haskellian import AsynIter, asyn_iter as AI

@AI.lift
async def gen():
  for i in range(10):
    yield i

await gen() \
  .map(lambda x: 2*x) \
  .filter(lambda x: x % 2 == 0) \
  .batch(2) \
  .skip(1) \
  .sync()
```