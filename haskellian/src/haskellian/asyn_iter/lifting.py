from haskellian import asyn_iter as AI
from typing_extensions import ParamSpec, Callable, AsyncIterable, TypeVar
from functools import wraps

A = TypeVar('A')

P = ParamSpec('P')
def lift(f: Callable[P, AsyncIterable[A]]) -> Callable[P, AI.AsyncIter[A]]:
  """Lift a function `f` to return an `AsyncIter`"""
  @wraps(f)
  def _f(*args: P.args, **kwargs: P.kwargs) -> AI.AsyncIter[A]:
    return AI.AsyncIter(f(*args, **kwargs))
  return _f