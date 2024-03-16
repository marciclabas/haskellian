from typing import Iterable, TypeVar

A = TypeVar('A')

def pick(inds: Iterable[int], xs: list[A]) -> list[A]:
    """Pick `xs` values at indices `inds`
    - E.g. `pick([1, 2, 4], ['a', 'b', 'c', 'd', 'e', 'f', 'g']) = ['b', 'c', 'e']`"""
    return [xs[i] for i in inds]