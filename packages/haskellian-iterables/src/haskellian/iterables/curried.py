import builtins
from typing import Iterable, Callable, TypeVar
import itertools
from ramda import curry

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
Etc = TypeVar('Etc')


@curry
def map(f: Callable[[A], B], xs: Iterable[A]) -> Iterable[B]:
    """Curried version of `map`"""
    return builtins.map(f, xs)

@curry
def filter(p: Callable[[A], bool], xs: Iterable[A]) -> Iterable[B]:
    """Curried version of `filter`"""
    return builtins.filter(p, xs)

@curry
def min(xs: Iterable[A], key: Callable[[A], B] = None) -> Iterable[A]:
    """Curried version of `min`"""
    return builtins.min(xs, key=key)

@curry
def max(xs: Iterable[A], key: Callable[[A], B] = None) -> Iterable[A]:
    """Curried version of `max`"""
    return builtins.max(xs, key=key)

@curry
def sorted(xs: Iterable[A], key: Callable[[A], B] = None, reverse: bool = False) -> Iterable[A]:
    """Curried version of `sorted`"""
    return builtins.sorted(xs, key=key, reverse=reverse)

def flatten(xs: Iterable[Iterable[A]]) -> Iterable[A]:
    """Single-level list flattening"""
    return itertools.chain.from_iterable(xs)

@curry
def flatmap(f: Callable[[A], Iterable[B]], xs: Iterable[A]) -> Iterable[B]:
    """Monadic `bind` on iterables. Aka `>>=`, `chain`"""
    return flatten(map(f, xs))

@curry
def starmap(f: Callable[[A, B, Etc], C], xs: Iterable[tuple[A, B, Etc]]) -> Iterable[C]:
    """Curried version of `starmap`"""
    return itertools.starmap(f, xs)
