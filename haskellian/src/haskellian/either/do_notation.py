from typing_extensions import Callable, TypeVar, ParamSpec, Generic
from functools import wraps
from dataclasses import dataclass
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
  def __call__(self, fn: Callable[P, R]) -> Callable[P, Either[L, R]]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
      try:
        return Right(fn(*args, **kwargs))
      except IsLeft as e:
        return Left(e.value)
    return wrapper