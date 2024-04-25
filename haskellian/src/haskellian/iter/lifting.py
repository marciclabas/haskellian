from haskellian import DEBUG_IMPORTS, iter as I
if DEBUG_IMPORTS:
  print('Import:', __name__)
from typing_extensions import ParamSpec, Callable, Iterable, TypeVar
from functools import wraps

A = TypeVar('A')

P = ParamSpec('P')
def lift(func: Callable[P, Iterable[A]]) -> Callable[P, I.Iter[A]]:
  """Lift an iterable function `func` to return an `Iter`"""
  @wraps(func)
  def _f(*args: P.args, **kwargs: P.kwargs) -> I.Iter[A]:
    return I.Iter(func(*args, **kwargs))
  return _f