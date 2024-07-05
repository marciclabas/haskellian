from typing import TypeVar, Callable, Iterable
from collections import defaultdict

K = TypeVar('K')
V = TypeVar('V')

def group_by(f: Callable[[V], K], xs: Iterable[V]) -> dict[K, list[V]]:
  """Group elements by a function"""
  d = defaultdict(list)
  for x in xs:
    d[f(x)].append(x)
  return dict(d)