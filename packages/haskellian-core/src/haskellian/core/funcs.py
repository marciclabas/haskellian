from typing import TypeVar, Callable, Iterable
from functools import reduce, wraps

A = TypeVar('A')
B = TypeVar('B')


def pipe(x: A, *funcs: Callable[[A], B]) -> B:
  """Apply to `x` a left-to-right composition of `funcs`
  >>> pipe('  hello ', str.strip, str.title) # 'Hello'
  """
  return reduce(lambda x, f: f(x), funcs, x)

def flow(*funcs: Callable[[A], B]) -> Callable[[A], B]:
  """Left-to-right composition of `funcs`
  >>> func = flow(str.strip, str.title) # same as: func = lambda s: s.strip().title()
  """
  return lambda x: pipe(x, *funcs)


def safe(f: Callable[[], A]) -> A | None:
  """Tries to return `f()`, otherwise `None`"""
  try:
    return f()
  except:
    ...

def listify(func: Callable[[A], Iterable[B]]) -> Callable[[A], list[B]]:
    """Make a generator return a list
    
    ```
    @listify
    def mygenerator():
      for x in range(3):
        yield x

    mygenerator() # [0, 1, 2]
    ```
    """
    @wraps(func)
    def _f(*args, **kwargs):
        return list(func(*args, **kwargs))
    return _f