from typing import TypeVar, Iterable, Callable
import itertools
import builtins
import ramda as R

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
Etc = TypeVar('Etc')

def unzipg(xs: Iterable[tuple[A, ...]]) -> tuple[Iterable[A], ...]:
    """`[(a, b, ...)] -> ([a], [b], ...)`\nLike `unzip` but returns a tuple of generators"""
    return tuple(zip(*xs))

def unzip(xs: Iterable[tuple[A, ...]]) -> tuple[Iterable[A], ...]:
    """`[(a, b, ...)] -> ([a], [b], ...)`"""
    return tuple(map(list, zip(*xs)))

@R.curry
def map(f: Callable[[A], B], xs: Iterable[A]) -> Iterable[B]:
    return builtins.map(f, xs)

@R.curry
def filter(p: Callable[[A], bool], xs: Iterable[A]) -> Iterable[B]:
    return builtins.filter(p, xs)

@R.curry
def flatten(xs: Iterable[Iterable[A]]) -> Iterable[A]:
    return itertools.chain.from_iterable(xs)

@R.curry
def flatmap(f: Callable[[A], Iterable[B]], xs: Iterable[A]) -> Iterable[B]:
    return flatten(map(f, xs))

@R.curry
def starmap(f: Callable[[A, B, Etc], C], xs: Iterable[tuple[A, B, Etc]]) -> Iterable[C]:
    return itertools.starmap(f, xs)

@R.curry
def take(n: int | None, xs: Iterable[A]) -> Iterable[A]:
    return itertools.islice(xs, n)

@R.curry
def skip(n: int, xs: Iterable[A]) -> Iterable[A]:
    return itertools.islice(xs, n, None)

def head(xs: Iterable[A]) -> A | None:
    return next(xs, None)
    
def tail(xs: Iterable[A]) -> Iterable[A]:
    return skip(1, xs)

@R.curry
def split(n: int, xs: Iterable[A]) -> tuple[list[A], Iterable[A]]:
    """Splits `xs` into a list of the first `n` and a generator of the rest
    - e.g: `split(3, [1,2,3,4,5]) == ([1, 2, 3], generator(4, 5))`"""
    it = iter(xs)
    init = list(take(n, it))
    return init, (x for x in it)

def fst(t: tuple[A, ...]) -> A:
    x, *_ = t
    return x

def snd(t: tuple[A, ...]) -> A:
    _, x, *_ = t
    return x

@R.curry
def batch(n: int, iterable: Iterable[A]) -> Iterable[tuple[A]]:
    it = iter(iterable)
    while b := tuple(itertools.islice(it, n)):
        yield b
        
@R.curry
def min(xs: Iterable[A], key: Callable[[A], B] = None) -> Iterable[A]:
    return builtins.min(xs, key=key)

@R.curry
def sorted(xs: Iterable[A], key: Callable[[A], B] = None, reverse: bool = False) -> Iterable[A]:
    return builtins.sorted(xs, key=key, reverse=reverse)

def uncons(xs: Iterable[A]) -> tuple[A | None, Iterable[A]]:
    """`uncons([1, 2, 3]) = (1, [2, 3])`"""
    it = iter(xs)
    x = next(it, None)
    return x, (x for x in it)

def pairwise(xs: Iterable[A]) -> Iterable[A]:
    """`pairwise([1, 2, 3, 4, 5]) = [(1, 2), (2, 3), (3, 4), (4, 5)]`
    - `pairwise([]) = []`
    - `pairwise([x]) = []`
    """
    x0, tail = uncons(xs)
    for x1 in tail:
        yield x0, x1
        x0 = x1
        
def transpose(xs: Iterable[Iterable[A]]) -> Iterable[Iterable[A]]:
    """`transpose([[1, 2], [3, 4], [5, 6]]) = [[1, 2, 3], [4, 5, 6]]`"""
    return zip(*xs)

def pick(inds: Iterable[int], xs: list[A]) -> list[A]:
    """Pick `xs` values at indices `inds`
    >>> pick([1, 4, 9], list(range(10))) == [1, 4, 9]"""
    return [xs[i] for i in inds]