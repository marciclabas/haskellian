import builtins
from typing_extensions import Callable, TypeVar, Iterable, TypeGuard, overload

A = TypeVar('A')
B = TypeVar('B')

def map(f: Callable[[A], B]) -> Callable[[Iterable[A]], Iterable[B]]:
  return lambda xs: builtins.map(f, xs)

@overload
def filter(p: Callable[[A], TypeGuard[B]]) -> Callable[[Iterable[A]], Iterable[B]]: ...
@overload
def filter(p: Callable[[A], bool]) -> Callable[[Iterable[A]], Iterable[A]]: ...
def filter(p): # type: ignore
  return lambda xs: builtins.filter(p, xs)

def sorted(key: Callable[[A], B] | None = None, reverse: bool = False) -> Callable[[Iterable[A]], Iterable[A]]:
  return lambda xs: builtins.sorted(xs, key=key, reverse=reverse) # type: ignore

def max(key: Callable[[A], B] | None = None) -> Callable[[Iterable[A]], A]:
  return lambda xs: builtins.max(xs, key=key, default=None) # type: ignore

def min(key: Callable[[A], B] | None = None) -> Callable[[Iterable[A]], A]:
  return lambda xs: builtins.min(xs, key=key, default=None) # type: ignore
