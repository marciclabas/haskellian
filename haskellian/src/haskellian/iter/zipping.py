from haskellian import DEBUG_IMPORTS, iter as I
if DEBUG_IMPORTS:
  print('Import:', __name__)
from typing_extensions import Iterable, TypeVar, overload

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

@overload
def unzip(xs: Iterable[tuple[A, B]]) -> tuple[list[A], list[B]]: ...
@overload
def unzip(xs: Iterable[tuple[A, B, C]]) -> tuple[list[A], list[B], list[C]]: ...
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
