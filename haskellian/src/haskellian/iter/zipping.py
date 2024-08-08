from haskellian import iter as I
from typing_extensions import Iterable, TypeVar, overload, Sequence

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
D = TypeVar('D')
E = TypeVar('E')
F = TypeVar('F')

@overload
def unzip(xs: Iterable[tuple[A, B]]) -> tuple[list[A], list[B]]: ...
@overload
def unzip(xs: Iterable[tuple[A, B, C]]) -> tuple[list[A], list[B], list[C]]: ...
@overload
def unzip(xs: Iterable[tuple[A, B, C, D]]) -> tuple[list[A], list[B], list[C], list[D]]: ...
@overload
def unzip(xs: Iterable[tuple[A, B, C, D, E]]) -> tuple[list[A], list[B], list[C], list[D], list[E]]: ...
@overload
def unzip(xs: Iterable[tuple[A, B, C, D, E, F]]) -> tuple[list[A], list[B], list[C], list[D], list[E], list[F]]: ...
@overload
def unzip(xs: Iterable[tuple[A, ...]]) -> tuple[list[A], ...]: ...
def unzip(xs):
    """`[(a, b, ...)] -> ([a], [b], ...)`"""
    return tuple(map(list, zip(*xs))) # type: ignore

def uncons(xs: Iterable[A]) -> tuple[A | None, I.Iter[A]]:
    """`uncons([x, *xs]) = (x, xs)`"""
    it = iter(xs)
    x = next(it, None)
    return x, I.Iter(it)

@I.lift
def pairwise(xs: Iterable[A]) -> Iterable[tuple[A, A]]:
    """`pairwise([x1, x2, x3, x4, ...]) = [(x1, x2), (x2, x3), (x3, x4), ...]`
    - `pairwise([]) = []`
    - `pairwise([x]) = []`
    """
    x0, tail = uncons(xs)
    for x1 in tail:
        yield x0, x1 # type: ignore (`x0` won't be `None` if there's some element in `tail`)
        x0 = x1

@I.lift
def interleave(xs: Sequence[tuple[int, Iterable[A]]]) -> Iterable[A]:
  """Interleave multiple iterators based on their weight.
  - `(weight, iter) = xs[i]`: `iter` is yielded `weight` times before moving to the next iterator.
  """
  weights, iters = I.unzip(xs)
  iters = [iter(it) for it in iters]
  weights = list(weights)
  while True:
    for i, (w, it) in enumerate(zip(weights, iters)):
      try:
        for _ in range(w):
          yield next(it)
      except StopIteration:
        weights.pop(i)
        iters.pop(i)
        if not weights:
          return