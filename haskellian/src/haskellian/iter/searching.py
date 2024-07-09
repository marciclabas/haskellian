from typing import Iterable, Sequence, TypeVar, Callable

A = TypeVar('A')

def find_idx(p: Callable[[A], bool], xs: Iterable[A]) -> int | None:
  for i, x in enumerate(xs):
    if p(x):
      return i

def find(p: Callable[[A], bool], xs: Iterable[A]) -> A | None:
  for x in xs:
    if p(x):
      return x
    
def find_last_idx(p: Callable[[A], bool], xs: Sequence[A]) -> int | None:
  for i, x in enumerate(reversed(xs)):
    if p(x):
      return len(xs) - i - 1

def find_last(p: Callable[[A], bool], xs: Sequence[A]) -> A | None:
  for x in reversed(xs):
    if p(x):
      return x