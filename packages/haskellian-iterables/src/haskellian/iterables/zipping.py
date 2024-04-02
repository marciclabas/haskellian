from typing import Iterable, TypeVar

A = TypeVar('A')

def unzipg(xs: Iterable[tuple[A, ...]]) -> tuple[Iterable[A], ...]:
    """`[(a, b, ...)] -> ([a], [b], ...)`
    - Like `unzip` but returns a tuple of generators"""
    return tuple(zip(*xs))

def unzip(xs: Iterable[tuple[A, ...]]) -> tuple[Iterable[A], ...]:
    """`[(a, b, ...)] -> ([a], [b], ...)`"""
    return tuple(map(list, zip(*xs)))

def uncons(xs: Iterable[A]) -> tuple[A | None, Iterable[A]]:
    """`uncons([x, *xs]) = (x, xs)`"""
    it = iter(xs)
    x = next(it, None)
    return x, (x for x in it)

def pairwise(xs: Iterable[A]) -> Iterable[A]:
    """`pairwise([x1, x2, x3, x4, ...]) = [(x1, x2), (x2, x3), (x3, x4), ...]`
    - `pairwise([]) = []`
    - `pairwise([x]) = []`
    """
    x0, tail = uncons(xs)
    for x1 in tail:
        yield x0, x1
        x0 = x1
