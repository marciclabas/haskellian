# `either`

The `either` package provides both functions and an `Either` class, that allows both method chaining and do notation style syntax.

## `Either[L, R]`

`Either[L, R]` is roughly defined as:

```python
class Left(Generic[L]):
  value: L
  tag: Literal['left']

class Right(Generic[R]):
  value: R
  tag: Literal['right']

Either[L, R] = Left[L] | Right[R]
```

### Do Notation

Thought it supports both method chaining and `either.tag == 'left'` branching, the most common way to use an either is with a sort of do notation:

```python
from haskellian import either as E, Either

def fetch_this() -> Either[KeyError, str]:
  ...

def fetch_that() -> Either[ValueError, str]:
  ...

@E.do[KeyError|ValueError]()
def do_function() -> str:
  this = fetch_this().unwrap() # str
  that = fetch_that().unwrap() # str
  return f'{this} and {that}'

do_function() # Either[KeyError|ValueError, str]
```

If you're familiar with Rust's `?` operator, this should be familiar.

## Functions

The `either` module has just a few utility functions:

::: haskellian.either.funcs

Next up, [`asyn_iter`](asyn-iter.md)