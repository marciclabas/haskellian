from typing_extensions import Callable, TypeVar, ParamSpec, overload
from functools import reduce

A = ParamSpec('A')
B = TypeVar('B')
C = TypeVar('C')
D = TypeVar('D')
E = TypeVar('E')
F = TypeVar('F')
G = TypeVar('G')
H = TypeVar('H')
I = TypeVar('I')

@overload
def flow(
  f1: Callable[A, B],
  f2: Callable[[B], C]
) -> Callable[A, C]: ...

@overload
def flow(
  f1: Callable[A, B],
  f2: Callable[[B], C],
  f3: Callable[[C], D]
) -> Callable[A, D]: ...

@overload
def flow(
  f1: Callable[A, B],
  f2: Callable[[B], C],
  f3: Callable[[C], D],
  f4: Callable[[D], E]
) -> Callable[A, E]: ...

@overload
def flow(
  f1: Callable[A, B],
  f2: Callable[[B], C],
  f3: Callable[[C], D],
  f4: Callable[[D], E],
  f5: Callable[[E], F]
) -> Callable[A, F]: ...

@overload
def flow(
  f1: Callable[A, B],
  f2: Callable[[B], C],
  f3: Callable[[C], D],
  f4: Callable[[D], E],
  f5: Callable[[E], F],
  f6: Callable[[F], G]
) -> Callable[A, G]: ...

@overload
def flow(
  f1: Callable[A, B],
  f2: Callable[[B], C],
  f3: Callable[[C], D],
  f4: Callable[[D], E],
  f5: Callable[[E], F],
  f6: Callable[[F], G],
  f7: Callable[[G], H]
) -> Callable[A, H]: ...

@overload
def flow(
  f1: Callable[A, B],
  f2: Callable[[B], C],
  f3: Callable[[C], D],
  f4: Callable[[D], E],
  f5: Callable[[E], F],
  f6: Callable[[F], G],
  f7: Callable[[G], H],
  f8: Callable[[H], I]
) -> Callable[A, I]: ...

def flow(*fs: Callable): # type: ignore
  return lambda x: reduce(lambda x, f: f(x), fs, x)
