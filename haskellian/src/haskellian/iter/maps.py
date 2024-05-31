from typing import TypeVar, Sequence, Mapping

A = TypeVar('A')
B = TypeVar('B')

def pluck(xs: Sequence[Mapping[A, B]], key: A) -> Sequence[B]:
  return [ x[key] for x in xs ]