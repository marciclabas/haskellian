from dataclasses import dataclass
from typing_extensions import Generic, TypeVar, Callable, TypeGuard, Iterator, Iterable, overload, Any, Literal
from haskellian import iter as I, Monad

A = TypeVar('A', covariant=True)
B = TypeVar('B')

@dataclass
class Iter(Monad[A], Iterator[A], Generic[A]):
  
  def __init__(self, xs: Iterable[A] = []):
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
    
  def empty(self) -> bool:
    x, xs = I.split(1, self.xs)
    self.xs = I.flatten([x, xs])
    return len(x) == 0

  def __next__(self) -> A:
    for x in self.xs:
      return x
    raise StopIteration()

  @classmethod
  def of(cls, value: B) -> 'Iter[B]':
    return Iter([value])
  
  def bind(self, f: Callable[[A], Iterable[B]]) -> 'Iter[B]': # type: ignore
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

  @overload
  def batch(self, n: int) -> 'Iter[tuple[A, ...]]': ...
  @overload
  def batch(self, n: int, *, lazy: Literal[True]) -> 'Iter[Iter[A]]': ...
  def batch(self, n: int, *, lazy: bool = False):
    return I.lazy_batch(n, self) if lazy else I.batch(n, self)
  
  @overload
  def shard(self, min_size: float, size: Callable[[A], float]) -> 'Iter[list[A]]': ...
  @overload
  def shard(self, min_size: float, size: Callable[[A], float], *, lazy: Literal[True]) -> 'Iter[Iter[A]]': ...
  def shard(self, min_size: float, size: Callable[[A], float], *, lazy: bool = False):
    """Shards `self` into groups of at least `min_size` based on `size` (last shard may have less)"""
    return I.lazy_shard(min_size, size, self) if lazy else I.shard(min_size, size, self)
  
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
  
  def every(self, n: int) -> 'Iter[A]':
    return I.every(n, self)
  
  def take_while(self, f: Callable[[A], bool]) -> 'Iter[A]':
    return I.take_while(f, self)
  
  def at(self, i: int) -> A | None:
    return self.skip(i).head()

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
  
  def find(self, p: Callable[[A], bool]) -> A | None:
    return I.find(p, self)
  
  def find_last_idx(self, p: Callable[[A], bool]) -> int | None:
    return I.find_last_idx(p, list(self))
  
  def find_last(self, p: Callable[[A], bool]) -> A | None:
    return I.find_last(p, list(self))

  def tap(self, f: Callable[[A], Any]) -> 'Iter[A]':
    return I.tap(f, self)

  def pad(self, n: int, fill: B) -> 'Iter[A|B]':
    return I.pad(n, fill, self)

  def sync(self) -> list[A]:
    return list(self.xs)
  
  def len(self) -> int:
    return len(list(self))

  @overload
  def append(self, x: A) -> 'Iter[A]': ... # type: ignore
  @overload
  def append(self, x: B) -> 'Iter[A|B]': ...
  def append(self, x): # type: ignore
    return self.extend([x])

  @overload
  def extend(self, xs: Iterable[A]) -> 'Iter[A]': ...
  @overload
  def extend(self, xs: Iterable[A|B]) -> 'Iter[A|B]': ...
  def extend(self, xs): # type: ignore
    return I.flatten([self, xs])
  
  def shuffle(self, shuffle_size: int) -> 'Iter[A]':
    return I.shuffle(self, shuffle_size)
  
  def i(self, f: Callable[['Iter[A]'], Iterable[B]]) -> 'Iter[B]':
    """Apply an arbitrary iterable function"""
    return Iter(f(self))
  