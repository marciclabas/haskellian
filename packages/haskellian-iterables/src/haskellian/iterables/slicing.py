from typing import TypeVar, Iterable, Callable
import itertools
from ramda import curry

A = TypeVar('A')

def fst(t: tuple[A, ...]) -> A:
	"""`fst((a, _)) = a`"""
	x, *_ = t
	return x

def snd(t: tuple[A, ...]) -> A:
	"""`snd((_, b)) = b`"""
	_, x, *_ = t
	return x

def head(xs: Iterable[A]) -> A | None:
  """`head([x, *_]) = x`"""
  for x in xs:
    return x
  
def tail(xs: Iterable[A]) -> Iterable[A]:
	"""`tail([_, *xs]) = xs`"""
	return skip(1, xs)

@curry
def take(n: int | None, xs: Iterable[A]) -> Iterable[A]:
	"""`take(n, [x1, ..., xn, *_]) = [x1, ..., xn]`"""
	return itertools.islice(xs, n)

@curry
def take_while(pred: Callable[[A], bool], xs: Iterable[A]) -> Iterable[A]:
	for x in xs:
		if not pred(x):
			return
		yield x
    
@curry
def skip(n: int, xs: Iterable[A]) -> Iterable[A]:
	"""`skip(n, [x1, ..., xn, *xs]) = xs`"""
	return itertools.islice(xs, n, None)

