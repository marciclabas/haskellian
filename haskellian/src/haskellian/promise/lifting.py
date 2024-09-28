from haskellian import promise as P
from typing_extensions import ParamSpec, Callable, Awaitable, TypeVar
from functools import wraps

A = TypeVar('A')
Ps = ParamSpec('Ps')

def lift(f: Callable[Ps, Awaitable[A]]) -> Callable[Ps, P.Promise[A]]:
  """Lift an async function `f` to return a `Promise`"""
  @wraps(f)
  def _f(*args: Ps.args, **kwargs: Ps.kwargs) -> P.Promise[A]:
    return P.Promise(f(*args, **kwargs))
  return _f