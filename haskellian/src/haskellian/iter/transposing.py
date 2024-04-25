from typing_extensions import Iterable, TypeVar
from itertools import zip_longest

A = TypeVar('A')

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