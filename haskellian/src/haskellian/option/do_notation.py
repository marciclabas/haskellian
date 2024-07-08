from typing_extensions import Callable, TypeVar, ParamSpec, Generic, overload, Coroutine, Awaitable
from inspect import iscoroutinefunction
from functools import wraps

T = TypeVar('T')
P = ParamSpec('P')

class IsNone(BaseException):
  ...

def unsafe(x: T | None) -> T:
  if x is None:
    raise IsNone()
  return x

@overload
def do(fn: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
  ...
@overload
def do(fn: Callable[P, T]) -> Callable[P, T | None]:
  ...
def do(fn): # type: ignore
  """Lift a function with do notation
  ```
  @do
  def safe_sum(a: int | None, b: int | None):
    return O.unsafe(a) + O.unsafe(b)

  safe_sum(1, 2) # 3
  safe_sum(None, 2) # None
  safe_sum(1, None) # None
  safe_sum(None, None) # None
  ```
  """
  if iscoroutinefunction(fn):
    @wraps(fn)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs):
      try:
        return await fn(*args, **kwargs)
      except IsNone:
        return None
    return _wrapper
  else:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
      try:
        return fn(*args, **kwargs)
      except IsNone:
        return None
    return wrapper