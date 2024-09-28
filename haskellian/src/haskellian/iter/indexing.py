from typing_extensions import Iterable, TypeVar

A = TypeVar('A')

def at(i: int, xs: list[int]) -> int | None:
  """Safe list indexing"""
  try:
    return xs[i]
  except IndexError:
    ...

def pick(indices: Iterable[int], xs: list[A]) -> list[A]:
  """Pick `xs` values at indices `indices`
  - E.g. `pick([1, 2, 4], ['a', 'b', 'c', 'd', 'e', 'f', 'g']) = ['b', 'c', 'e']`"""
  return [xs[i] for i in indices]