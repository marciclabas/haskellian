from haskellian import DEBUG_IMPORTS
if DEBUG_IMPORTS:
  print('Import:', __name__)
from dataclasses import dataclass
from typing_extensions import Generic, TypeVar, Callable, TypeGuard, Iterator, Iterable, overload, Any
from itertools import islice
from haskellian import iter as I, Monad, Pipe

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
  
  def flatmap(self, f: Callable[[A], Iterable[B]] = lambda x: x) -> 'Iter[B]': # type: ignore
    """Acts like `flatten` by default (`f` defaults to the identity)"""
    return self.bind(f)
  
  def iflatmap(self, f: Callable[[int, A], Iterable[B]]) -> 'Iter[B]':
    """`flatmap` with indices"""
    return self.enumerate().flatmap(lambda xs: f(*xs))
  
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

  @overload
  def reduce(self, f: Callable[[B, A], B], init: B) -> B: ...
  @overload
  def reduce(self, f: Callable[[A, A], A]) -> A | None: ...

  def reduce(self, f, init=None): # type: ignore
    from functools import reduce
    if init is None:
      init = self.head()
      if init is not None:
        return reduce(f, self, init)
    else:
      return reduce(f, self, init)

  
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
  
  def skip(self, n: int) -> 'Iter[A]':
    return I.skip(n, self)
  
  def take_while(self, f: Callable[[A], bool]) -> 'Iter[A]':
    return I.take_while(f, self)
  
  def at(self, i: int) -> A | None:
    for x in islice(self, i, None):
      return x

  def pairwise(self) -> 'Iter[tuple[A, A]]':
    return I.pairwise(self)
  
  def enumerate(self) -> 'Iter[tuple[int, A]]':
    return Iter(enumerate(self))
  
  def sort(self, key: Callable[[A], Any] | None = None, reverse: bool = False) -> 'Iter[A]':
    """Like `sorted`, but returns an `Iter`"""
    return Iter(sorted(self, key=key, reverse=reverse)) # type: ignore
  
  def sorted(self, key: Callable[[A], Any] | None = None, reverse: bool = False) -> list[A]:
    return sorted(self, key=key, reverse=reverse) # type: ignore
  
  def min(self, key: Callable[[A], Any] | None = None) -> A | None:
    return min(self, key=key, default=None) # type: ignore
  
  def max(self, key: Callable[[A], Any] | None = None) -> A | None:
    return max(self, key=key, default=None) # type: ignore
  
  def find_idx(self, p: Callable[[A], bool]) -> int | None:
    return I.find_idx(p, self)
  
  def find_last_idx(self, p: Callable[[A], bool]) -> int | None:
    return I.find_last_idx(p, list(self))

  def tap(self, f: Callable[[A], Any]) -> 'Iter[A]':
    return I.tap(f, self)

  def sync(self) -> list[A]:
    return list(self.xs)
  
  def len(self) -> int:
    return len(list(self))
  
  def i(self, f: Callable[['Iter[A]'], Iterable[B]]) -> 'Iter[B]':
    """Apply an arbitrary iterable function"""
    return Iter(f(self))
  
  def f(self, f: Callable[['Iter[A]'], B]) -> Pipe[B]:
    """Apply an arbitrary function into a `Pipe`"""
    return Pipe(f(self))