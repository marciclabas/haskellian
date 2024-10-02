from typing_extensions import Callable, TypeVar, ParamSpec, Generic, overload, Coroutine, Awaitable
from inspect import iscoroutinefunction
from functools import wraps
from .either import Either, Left, Right, IsLeft

L = TypeVar('L')
R = TypeVar('R')
P = ParamSpec('P')

class do(Generic[L]):
  """Lift a function with do notation
  ```
  @do[LeftType]()
  def myfn(e: Either[LeftType, int]):
    value = e.unsafe()
    return value + 1

  myfn(Left('err')) # Left('err')
  myfn(Right(1)) # Right(2)
  ```
  """
  @overload
  def __call__(self, fn: Callable[P, Coroutine[None, None, R]]) -> Callable[P, Coroutine[None, None, Either[L, R]]]: # type: ignore
    ...
  @overload
  def __call__(self, fn: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[Either[L, R]]]: # type: ignore
    ...
  @overload
  def __call__(self, fn: Callable[P, R]) -> Callable[P, Either[L, R]]:
    ...
  
  def __call__(self, fn): # type: ignore
    if iscoroutinefunction(fn):
      @wraps(fn)
      async def _wrapper(*args: P.args, **kwargs: P.kwargs):
        try:
          return Right(await fn(*args, **kwargs))
        except IsLeft as e:
          return Left(e.value)
      return _wrapper
    else:
      @wraps(fn)
      def wrapper(*args: P.args, **kwargs: P.kwargs):
        try:
          return Right(fn(*args, **kwargs))
        except IsLeft as e:
          return Left(e.value)
      return wrapper