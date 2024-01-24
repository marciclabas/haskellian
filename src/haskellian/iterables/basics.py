import builtins
from typing import Iterable, Callable, TypeVar
import itertools
import ramda as R

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
Etc = TypeVar('Etc')

def iterable(x) -> bool:
    """Is `x` iterable? (`str` is considered **not iterable**)"""
    return isinstance(x, Iterable) and not isinstance(x, str)

@R.curry
def map(f: Callable[[A], B], xs: Iterable[A]) -> Iterable[B]:
    return builtins.map(f, xs)

@R.curry
def filter(p: Callable[[A], bool], xs: Iterable[A]) -> Iterable[B]:
    return builtins.filter(p, xs)

@R.curry
def min(xs: Iterable[A], key: Callable[[A], B] = None) -> Iterable[A]:
    return builtins.min(xs, key=key)

@R.curry
def max(xs: Iterable[A], key: Callable[[A], B] = None) -> Iterable[A]:
    return builtins.max(xs, key=key)

@R.curry
def sorted(xs: Iterable[A], key: Callable[[A], B] = None, reverse: bool = False) -> Iterable[A]:
    return builtins.sorted(xs, key=key, reverse=reverse)

@R.curry
def flatten(xs: Iterable[Iterable[A]]) -> Iterable[A]:
    return itertools.chain.from_iterable(xs)

@R.curry
def flatmap(f: Callable[[A], Iterable[B]], xs: Iterable[A]) -> Iterable[B]:
    return flatten(map(f, xs))

@R.curry
def starmap(f: Callable[[A, B, Etc], C], xs: Iterable[tuple[A, B, Etc]]) -> Iterable[C]:
    return itertools.starmap(f, xs)

def range(end: int | None = None) -> Iterable[int]:
    """Possibly infinite range"""
    if end is None:
        i = 0
        while True:
            yield i
            i += 1
    else:
        for i in builtins.range(end):
            yield i