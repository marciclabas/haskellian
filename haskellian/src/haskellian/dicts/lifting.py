from haskellian import dicts as D
from typing_extensions import ParamSpec, Callable, Mapping, TypeVar
from functools import wraps

K = TypeVar('K')
V = TypeVar('V')
P = ParamSpec('P')

def lift(func: Callable[P, Mapping[K, V]]) -> Callable[P, D.Dict[K, V]]:
  """Lift a mapping function `func` to return a `Dict`"""
  @wraps(func)
  def _f(*args: P.args, **kwargs: P.kwargs) -> D.Dict[K, V]:
    return D.Dict(func(*args, **kwargs)) # type: ignore pylance wtf
  return _f
