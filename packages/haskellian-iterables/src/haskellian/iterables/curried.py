import builtins
from typing import Iterable, Callable, TypeVar, overload, TypeVarTuple
import itertools
from ramda import curry

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
As = TypeVarTuple('As')


def map(f: Callable[[A], B]):
    """Curried version of `map`"""
    def _curried(xs: Iterable[A]) -> Iterable[B]:
        return builtins.map(f, xs)
    return _curried

def filter(p: Callable[[A], bool]):
    """Curried version of `filter`"""
    def _curried(xs: Iterable[A]) -> Iterable[B]:
        return builtins.filter(p, xs)
    return _curried

def min(key: Callable[[A], B]):
    """Curried version of `min`"""
    def _curried(xs: Iterable[A]) -> A:
        return builtins.min(xs, key=key)
    return _curried

def max(key: Callable[[A], B]):
    """Curried version of `min`"""
    def _curried(xs: Iterable[A]) -> A:
        return builtins.max(xs, key=key)
    return _curried

def sorted(key: Callable[[A], B] = None, reverse: bool = False):
    """Curried version of `sorted`"""
    def _curried(xs: Iterable[A]) -> Iterable[A]:
        return builtins.sorted(xs, key=key, reverse=reverse)
    return _curried

def flatten(xs: Iterable[Iterable[A]]) -> Iterable[A]:
    """Single-level list flattening"""
    return itertools.chain.from_iterable(xs)

@overload
def flatmap(f: Callable[[A], Iterable[B]], xs: Iterable[A]) -> Iterable[B]: ...
@overload
def flatmap(f: Callable[[A], Iterable[B]]) -> Callable[[Iterable[A]], Iterable[B]]: ...
@curry
def flatmap(f, xs):
    """Monadic `bind` on iterables. Aka `>>=`, `chain`"""
    return flatten(map(f, xs))

def starmap(f: Callable[[*As], C]):
    """Curried version of `starmap`"""
    def _curried(xs: Iterable[tuple[*As]]) -> Iterable[C]:
        return itertools.starmap(f, xs)
    return _curried
