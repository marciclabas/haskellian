from typing_extensions import TypeVar, Literal, Callable, Iterable, overload, Any
from haskellian import iter as I
from .basics import isiterable

A = TypeVar('A')
B = TypeVar('B')

@overload
def ndmap(f: Callable[[A], B], xs: Iterable[Iterable[Iterable[A]]], depth: Literal[3]) -> list[list[list[B]]]: ...
@overload
def ndmap(f: Callable[[A], B], xs: Iterable[Iterable[Iterable[Iterable[A]]]], depth: Literal[4]) -> list[list[list[list[B]]]]: ...
@overload
def ndmap(f: Callable[[A], B], xs: Iterable[Iterable[A]], depth: Literal[2] = 2) -> list[list[B]]: ...
@overload
def ndmap(f: Callable[[A], B], xs: Iterable, depth: int) -> list: ...
def ndmap(f, xs, depth = 2):
  return f(xs) if depth == 0 else [ndmap(f, x, depth-1) for x in xs]

Range = int | tuple[int, int] | tuple[int, int, int]
@overload
def ndrange(rng1: Range) -> I.Iter[tuple[int]]: ...
@overload
def ndrange(rng1: Range, rng2: Range) -> I.Iter[tuple[int, int]]: ...
@overload
def ndrange(rng1: Range, rng2: Range, rng3: Range) -> I.Iter[tuple[int, int, int]]: ...
@overload
def ndrange(*ranges: Range) -> I.Iter[tuple[int, ...]]: ...
@I.lift
def ndrange(*ranges): # type: ignore
  """Like `range`, but returns an iterable of `n`-tuples instead of ints.
  
  So, instead of
  ```
  for i in range(m):
  for j in range(n):
    ...
  ```
  You can just do:
  ```
  for i, j in ndrange(m, n):
  ...
  ```
  
  And it also supports normal `(start, end)` or `(start, end, step)` ranges:
  ```
  for i, j in ndrange((-10, 0, 2), (4, 6)):
  ...
  # (-10, 4), (-10, 5), (-8, 4), (-8, 5), ...
  ```
  """
  def _ndrange(*ranges, inds = ()):
    if len(ranges) == 0:
      yield inds
    else:
      [r, *rs] = ranges
      rng = range(*r) if isiterable(r) else range(r)
      for i in rng:
        yield from _ndrange(*rs, inds=inds+(i,))
  
  yield from _ndrange(*ranges)

@I.lift
def _fixed_ndenumerate(xxs, depth: int, inds: tuple[int, ...] = ()):
  if depth == 0:
    yield inds, xxs
  else:
    for i, xs in enumerate(xxs):
      yield from _fixed_ndenumerate(xs, depth-1, inds + (i, ))

@I.lift
def _auto_ndenumerate(xxs, inds: tuple[int, ...] = ()):
  if not isiterable(xxs):
    yield inds, xxs
  else:
    for i, xs in enumerate(xxs):
      yield from _auto_ndenumerate(xs, inds + (i,))

@overload
def ndenumerate(xxs: Iterable[Iterable[A]], depth: Literal[2] | None = None) -> I.Iter[tuple[tuple[int, int], A]]: ...
@overload
def ndenumerate(xxs: Iterable[Iterable[Iterable[A]]], depth: Literal[3] | None = None) -> I.Iter[tuple[tuple[int, int, int], A]]: ...
@overload
def ndenumerate(xxs: Iterable, depth: int | None = None) -> I.Iter[tuple[tuple[int, ...], Any]]: ...
@I.lift
def ndenumerate(xxs, depth: int | None = None): # type: ignore
  """Like `enumerate`, but for nested iterables.
  
  So, instead of
  
  ```
  for i, xxs in enumerate(xxxs):
  for j, xs in enumerate(xxs):
    for k, x in enumerate(xs):
    ...
  ```
  
  You can just do
  
  ```
  for x, (i, j, k) in ndenumerate(xxxs):
  ...
  ```
  
  Note:
  - By default it unrolls all the way down until a none-iterable object is found.
  - If you want to iterate over iterables (e.g. lists, numpy arrays, tensors), you'll have to pass in a fixed `depth`
  """
  return _auto_ndenumerate(xxs) if depth is None else _fixed_ndenumerate(xxs, depth)

def _fixed_ndflat(xxs, depth: int):
  if depth == 0:
    yield xxs
  else:
    for xs in xxs:
      yield from _fixed_ndflat(xs, depth-1)
      
def _auto_ndflat(xxs):
  if not isiterable(xxs):
    yield xxs
  else:
    for xs in xxs:
      yield from _auto_ndflat(xs)
      
@overload
def ndflat(xxs: Iterable[Iterable[A]], depth: Literal[2] | None = None) -> I.Iter[I.Iter[A]]: ...
@overload
def ndflat(xxs: Iterable[Iterable[Iterable[A]]], depth: Literal[3] | None = None) -> I.Iter[A]: ...
@overload
def ndflat(xxs: Iterable, depth: int | None = None) -> I.Iter: ...
@I.lift
def ndflat(xxs: Iterable[Iterable[A]], depth: int | None = None): # type: ignore
  """`ndflat([[x1, x2], [x3, [x4]]]) = [x1, x2, x3, x4]`"""
  return _auto_ndflat(xxs) if depth is None else _fixed_ndflat(xxs, depth) # type: ignore