from typing import TypeVar, Iterable, Mapping

A = TypeVar('A')
B = TypeVar('B')

def pluck(xs: Iterable[Mapping[A, B]], key: A) -> Iterable[B]:
  """Extract values by key. Skips dicts without it."""
  for x in xs:
    if key in x:
      yield x[key]