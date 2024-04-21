from haskellian import DEBUG_IMPORTS
if DEBUG_IMPORTS:
  print('Import:', __name__)
from dataclasses import dataclass
from typing import Generic, TypeVar, Callable, TypeGuard, Iterator, Iterable, overload
from itertools import islice
from haskellian import iter as I, Monad

A = TypeVar('A', covariant=True)
B = TypeVar('B')

@dataclass
class Iter(Monad[A], Iterator[A], Generic[A]):
  
  def __init__(self, xs: Iterable[A]):
    self.xs = (x for x in xs)

  def __repr__(self):
    previewed, rest = I.split(5, self.xs)
    self.xs = I.flatten([previewed, rest])
    if len(previewed) == 0:
      return 'Iter([])'
    elif len(previewed) < 5:
      return f'Iter({previewed})'
    else:
      return f'Iter([{", ".join(str(x) for x in previewed)}, ...])'

  def __next__(self) -> A:
    for x in self.xs:
      return x
    raise StopIteration()

  @classmethod
  def of(cls, value: B) -> 'Iter[B]':
    return Iter([value])
  
  def bind(self, f: Callable[[A], Iterable[B]]) -> 'Iter[B]':
    return I.flatmap(f, self)
  
  flatmap = bind
  
  def map(self, f: Callable[[A], B]) -> 'Iter[B]':
    return Iter(map(f, self))
  
  fmap = map

  def __or__(self, f: Callable[[A], B]) -> 'Iter[B]':
    """Alias of `map`"""
    return self.map(f)
  
  @overload
  def filter(self, p: Callable[[A], TypeGuard[B]]) -> 'Iter[B]': ...
  @overload
  def filter(self, p: Callable[[A], bool]) -> 'Iter[A]': ...
  def filter(self, p): # type: ignore
    return Iter(filter(p, self))
  
  def batch(self, n: int) -> 'Iter[tuple[A, ...]]':
    return I.batch(n, self)
  
  def head(self) -> A | None:
    return I.head(self)
  
  def tail(self) -> 'Iter[A]':
    return I.tail(self)
  
  def uncons(self) -> tuple[A | None, 'Iter[A]']:
    return I.uncons(self)
  
  def split(self, n: int) -> 'tuple[Iter[A], Iter[A]]':
    xs, ys = I.split(n, self)
    return Iter(xs), Iter(ys)
  
  def take(self, n: int) -> 'Iter[A]':
    return I.take(n, self)
  
  def take_while(self, f: Callable[[A], bool]) -> 'Iter[A]':
    return I.take_while(f, self)
  
  def at(self, i: int) -> A | None:
    for x in islice(self, i, None):
      return x

  def pairwise(self) -> 'Iter[tuple[A, A]]':
    return I.pairwise(self)
  
  def enumerate(self) -> 'Iter[tuple[int, A]]':
    return Iter(enumerate(self))
  
  def sync(self) -> list[A]:
    return list(self.xs)
  