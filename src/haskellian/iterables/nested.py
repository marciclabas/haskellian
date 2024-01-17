from typing import Iterable, TypeVar
import ramda as R
from .basics import iterable

A = TypeVar('A')

def _fixed_ndenumerate(xxs: Iterable[Iterable[A]], depth: int, inds: tuple[int, ...] = ()) -> Iterable[tuple[A, tuple[int, ...]]]:
    if depth == 0:
        yield inds, xxs
    else:
        for i, xs in enumerate(xxs):
            yield from _fixed_ndenumerate(xs, depth-1, inds + (i, ))

def _auto_ndenumerate(xxs: Iterable[Iterable[A]], inds: tuple[int, ...] = ()) -> Iterable[tuple[A, tuple[int, ...]]]:
    if not iterable(xxs):
        yield inds, xxs
    else:
        for i, xs in enumerate(xxs):
            yield from _auto_ndenumerate(xs, inds + (i,))

@R.curry         
def ndenumerate(xxs: Iterable[Iterable[A]], depth: int | None = None) -> Iterable[tuple[tuple[int, ...], A]]:
    """`ndenumerate([[x1, x2], [x3]]) = [(x1, (0, 0)), (x2, (0, 1), (x3, (1, 0)))]`"""
    return _auto_ndenumerate(xxs) if depth is None else _fixed_ndenumerate(xxs, depth)

def _fixed_ndflat(xxs: Iterable[Iterable[A]], depth: int) -> Iterable[A]:
    if depth == 0:
        yield xxs
    else:
        for xs in xxs:
            yield from _fixed_ndflat(xs, depth-1)
            
def _auto_ndflat(xxs: Iterable[Iterable[A]]) -> Iterable[A]:
    if not iterable(xxs):
        yield xxs
    else:
        for xs in xxs:
            yield from _auto_ndflat(xs)
            
@R.curry
def ndflat(xxs: Iterable[Iterable[A]], depth: int | None = None) -> Iterable[Iterable[A]]:
    """`ndflat([[x1, x2], [x3, [x4]]]) = [x1, x2, x3, x4]`"""
    return _auto_ndflat(xxs) if depth is None else _fixed_ndflat(xxs, depth)

def transpose(xs: Iterable[Iterable[A]]) -> Iterable[Iterable[A]]:
    """`transpose([[1, 2], [3, 4], [5, 6]]) = [[1, 2, 3], [4, 5, 6]]`"""
    return zip(*xs)