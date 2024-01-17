from typing import Iterable, TypeVar

A = TypeVar('A')

def pick(inds: Iterable[int], xs: list[A]) -> list[A]:
    """Pick `xs` values at indices `inds`
    - `pick([1, 4, 9], list(range(10))) = [1, 4, 9]`"""
    return [xs[i] for i in inds]