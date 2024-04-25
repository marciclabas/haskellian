from typing_extensions import Callable, TypeVar, ParamSpec, overload
from functools import reduce

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
D = TypeVar('D')
E = TypeVar('E')
F = TypeVar('F')
G = TypeVar('G')
H = TypeVar('H')
I = TypeVar('I')

@overload
def pipe(
  x: A,
  f1: Callable[[A], B],
) -> B: ...

@overload
def pipe(
  x: A,
  f1: Callable[[A], B],
  f2: Callable[[B], C]
) -> C: ...

@overload
def pipe(
  x: A,
  f1: Callable[[A], B],
  f2: Callable[[B], C],
  f3: Callable[[C], D]
) -> D: ...

@overload
def pipe(
  x: A,
  f1: Callable[[A], B],
  f2: Callable[[B], C],
  f3: Callable[[C], D],
  f4: Callable[[D], E]
) -> E: ...

@overload
def pipe(
  x: A,
  f1: Callable[[A], B],
  f2: Callable[[B], C],
  f3: Callable[[C], D],
  f4: Callable[[D], E],
  f5: Callable[[E], F]
) -> F: ...

@overload
def pipe(
  x: A,
  f1: Callable[[A], B],
  f2: Callable[[B], C],
  f3: Callable[[C], D],
  f4: Callable[[D], E],
  f5: Callable[[E], F],
  f6: Callable[[F], G]
) -> G: ...

@overload
def pipe(
  x: A,
  f1: Callable[[A], B],
  f2: Callable[[B], C],
  f3: Callable[[C], D],
  f4: Callable[[D], E],
  f5: Callable[[E], F],
  f6: Callable[[F], G],
  f7: Callable[[G], H]
) -> H: ...

@overload
def pipe(
  x: A,
  f1: Callable[[A], B],
  f2: Callable[[B], C],
  f3: Callable[[C], D],
  f4: Callable[[D], E],
  f5: Callable[[E], F],
  f6: Callable[[F], G],
  f7: Callable[[G], H],
  f8: Callable[[H], I]
) -> I: ...

def pipe(x, *fs: Callable): # type: ignore
  return reduce(lambda x, f: f(x), fs, x)
