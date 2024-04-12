from typing import ParamSpec, Callable, AsyncIterable, TypeVar
from functools import wraps
from ..iter import AsyncIter

A = TypeVar('A')

P = ParamSpec('P')
def lift(f: Callable[P, AsyncIterable[A]]) -> Callable[P, AsyncIter[A]]:
  """Lift a function `f` to return an `AsyncIter`"""
  @wraps(f)
  def _f(*args: P.args, **kwargs: P.kwargs) -> AsyncIter[A]:
    return AsyncIter(f(*args, **kwargs))
  return _f