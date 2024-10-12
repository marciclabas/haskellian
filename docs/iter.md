# `iter`

The `iter` module provides both functions and an `Iter` class, a thin wrapper around generators that allows for lazy evaluation and chaining of operations.

## `Iter[T]`

The most common way to create `Iter`s is to "lift" generator functions:

```python
from haskellian import iter as I

@I.lift
def gen():
  for i in range(100000000):
    yield i

gen() # Iter[int]
```

### Method Chaining

Many common methods are available for chaining operations. For example:

```python
from haskellian import Iter

(Iter(range(100000000))
  .filter(lambda x: x % 2 == 0)
  .map(lambda x: x * 2)
  .skip(10)
  .enumerate()
  .every(4)
  .take(5)
  .sync())
# [(0, 40), (4, 56), (8, 72), (12, 88), (16, 104)]
```

## Functions

See the [reference](reference/iter.md) for a full list.


Next up, [`either`](either.md)