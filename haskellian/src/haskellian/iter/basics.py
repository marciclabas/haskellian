from typing_extensions import Iterable, TypeVar, Callable
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

@I.lift
def range(start: int = 0, end: int | None = None, step: int = 1) -> Iterable[int]:
  """Like `range`, but possibly infinite (if `end is None`)"""
  i = start
  while end is None or i < end:
    yield i
    i += step

@I.lift
def tap(f: Callable[[A], None], xs: Iterable[A]) -> Iterable[A]:
	for x in xs:
		f(x)
		yield x