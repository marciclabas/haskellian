from haskellian import DEBUG_IMPORTS
if DEBUG_IMPORTS:
  print('Import:', __name__)
from typing import Iterable, TypeVar, Callable
from itertools import chain
import haskellian.iter as I

A = TypeVar('A')
B = TypeVar('B')

def isiterable(x, str_iterable = False, bytes_iterable = False) -> bool:
  """Is `x` iterable?
  - `str_iterable`, `bytes_iterable`: whether `str` and `bytes` are considered iterable
  """
  return isinstance(x, Iterable) and \
    (not isinstance(x, str) or str_iterable) and \
    (not isinstance(x, bytes) or bytes_iterable)

@I.lift
def flatten(xs: Iterable[Iterable[A]]) -> Iterable[A]:
  """Single-level list flattening"""
  return chain.from_iterable(xs)

@I.lift
def flatmap(f: Callable[[A], Iterable[B]], xs: Iterable[A]) -> Iterable[B]:
  return flatten(map(f, xs))
