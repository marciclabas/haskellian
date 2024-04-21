# Haskellian

> The functional programming library you need

```bash
pip install haskellian
```

## Why
- Lazy imports + stub files -> great linting and 0 import time (thanks to [`lazy-loader`](https://github.com/scientific-python/lazy_loader))
- Monadic, method chaining style
- Great typing and overloads

```python
from haskellian import either as E, iter as I, promise as P, Pipe, asyn_iter as AI
```

#### `Pipe[A]` (simplest monad ever)

```python
Pipe('world hello') \
.f(str.title) \
.f(lambda s: s.split(' ')) \
.f(sorted) \
.f(', '.join) \
.value
# 'Hello, World'
```
#### `Iter[A]` (generators made ergonomic)

```python
I.Iter(range(100000000000)) \
.map(lambda x: 2*x) \
.filter(lambda x: x % 2 == 0) \
.batch(2) \
.tail()
#.sync() # don't recommend it...

# Iter([(4, 6), (8, 10), (12, 14), (16, 18), (20, 22), ...])
```

#### `Promise[A]` (awaitables made ergonomic)

```python
async def fetch_users() -> list[str]:
  ...
async def fetch_user(id) -> str:
  ...

await P.Promise(fetch_users()) \
.bind(lambda ids: P.all(map(fetch_user, ids))) \
.then(sorted)
```

#### `AsyncIter[A]`, `Either[L, R]` (self-explanatory at this point, right?)