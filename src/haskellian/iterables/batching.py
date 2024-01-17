from typing import Iterable, TypeVar
import itertools
import ramda as R
from .slicing import take

A = TypeVar('A')

@R.curry
def split(n: int, xs: Iterable[A]) -> tuple[list[A], Iterable[A]]:
    """Splits `xs` into a list of the first `n` and a generator of the rest
    - e.g: `split(3, [1,2,3,4,5]) == ([1, 2, 3], generator(4, 5))`"""
    it = iter(xs)
    init = list(take(n, it))
    return init, (x for x in it)


@R.curry
def batch(n: int, iterable: Iterable[A]) -> Iterable[tuple[A]]:
    it = iter(iterable)
    while b := tuple(itertools.islice(it, n)):
        yield b

