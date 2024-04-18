from typing import Iterable, TypeVar, Callable
from itertools import zip_longest
import ramda as R
from .basics import isiterable

A = TypeVar('A')
B = TypeVar('B')

@R.curry
def nested_map(f: Callable[[A], B], xs: Iterable[Iterable[A]], depth: int = 2) -> list[list[B]]:
    """`map` applied at a fixed depth. `nested_map(depth=1)` is equivalent to `map`, except it returns a `list`"""
    if depth == 0:
        return f(xs)  # Apply the function at the target depth
    else:
        return [nested_map(f, x, depth - 1) for x in xs]

def ndrange(*ranges: int | tuple[int, int] | tuple[int, int, int]) -> Iterable[tuple[int, ...]]:
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

def _fixed_ndenumerate(xxs: Iterable[Iterable[A]], depth: int, inds: tuple[int, ...] = ()) -> Iterable[tuple[A, tuple[int, ...]]]:
    if depth == 0:
        yield inds, xxs
    else:
        for i, xs in enumerate(xxs):
            yield from _fixed_ndenumerate(xs, depth-1, inds + (i, ))

def _auto_ndenumerate(xxs: Iterable[Iterable[A]], inds: tuple[int, ...] = ()) -> Iterable[tuple[A, tuple[int, ...]]]:
    if not isiterable(xxs):
        yield inds, xxs
    else:
        for i, xs in enumerate(xxs):
            yield from _auto_ndenumerate(xs, inds + (i,))

@R.curry         
def ndenumerate(xxs: Iterable[Iterable[A]], depth: int | None = None) -> Iterable[tuple[tuple[int, ...], A]]:
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

def _fixed_ndflat(xxs: Iterable[Iterable[A]], depth: int) -> Iterable[A]:
    if depth == 0:
        yield xxs
    else:
        for xs in xxs:
            yield from _fixed_ndflat(xs, depth-1)
            
def _auto_ndflat(xxs: Iterable[Iterable[A]]) -> Iterable[A]:
    if not isiterable(xxs):
        yield xxs
    else:
        for xs in xxs:
            yield from _auto_ndflat(xs)
            
@R.curry
def ndflat(xxs: Iterable[Iterable[A]], depth: int | None = None) -> Iterable[Iterable[A]]:
    """`ndflat([[x1, x2], [x3, [x4]]]) = [x1, x2, x3, x4]`"""
    return _auto_ndflat(xxs) if depth is None else _fixed_ndflat(xxs, depth)

def transpose(xs: Iterable[Iterable[A]]) -> list[list[A]]:
    """Transpose a 2d list, cropping to the shortest row. E.g:
    ```
    transpose([
        [1, 2],
        [3, 4],
        [5, 6]
    ]) == [
        [1, 3, 5],
        [2, 4, 6]
    ]
    ```
    but
    ```
    transpose([
        [1, 2],
        [3, 4],
        [5]
    ]) == [
        [1, 2, 3],
    ]
    ```
    """
    return list(zip(*xs))

def transpose_ragged(xs: Iterable[Iterable[A]]) -> list[list[A]]:
    """Like `transpose`, but resulting rows can be ragged (i.e. have different lengths). E.g:
    ```
    transpose([
        [1, 2],
        [3, 4],
        [5]
    ]) == [
        [1, 3, 5],
        [2, 4]
    ]
    ```"""
    return [[x for x in cols if x is not None] for cols in zip_longest(*xs)]
