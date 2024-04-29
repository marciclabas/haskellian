from typing import Iterable, Sequence, TypeVar, Callable

A = TypeVar('A')

def find_idx(p: Callable[[A], bool], xs: Iterable[A]) -> int | None:
  for i, x in enumerate(xs):
    if p(x):
      return i
    
def find_last_idx(p: Callable[[A], bool], xs: Sequence[A]) -> int | None:
  for i, x in enumerate(reversed(xs)):
    if p(x):
      return len(xs) - i - 1