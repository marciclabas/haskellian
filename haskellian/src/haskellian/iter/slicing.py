from haskellian import DEBUG_IMPORTS, iter as I
if DEBUG_IMPORTS:
  print('Import:', __name__)
from typing_extensions import TypeVar, TypeVarTuple, Iterable, Callable, Unpack
import itertools

A = TypeVar('A')
B = TypeVar('B')
As = TypeVarTuple('As')

def fst(t: tuple[A, Unpack[As]]) -> A:
	"""`fst((a, _)) = a`"""
	x, *_ = t
	return x

def snd(t: tuple[A, B, Unpack[As]]) -> B:
	"""`snd((_, b)) = b`"""
	_, x, *_ = t
	return x

def head(xs: Iterable[A]) -> A | None:
  """`head([x, *_]) = x`"""
  for x in xs:
    return x

@I.lift
def tail(xs: Iterable[A]) -> Iterable[A]:
	"""`tail([_, *xs]) = xs`"""
	return skip(1, xs)

def last(xs: Iterable[A]) -> A | None:
  """`head([x, *_]) = x`"""
  ys = list(xs)
  if len(ys) > 0:
    return ys[-1]

@I.lift
def take(n: int | None, xs: Iterable[A]) -> Iterable[A]:
	"""`take(n, [x1, ..., xn, *_]) = [x1, ..., xn]`"""
	return itertools.islice(xs, n)

@I.lift
def take_while(pred: Callable[[A], bool], xs: Iterable[A]) -> Iterable[A]:
	for x in xs:
		if not pred(x):
			return
		yield x

@I.lift
def drop_while(pred: Callable[[A], bool], xs: Iterable[A]) -> Iterable[A]:
	started = False
	for x in xs:
		if not started and not pred(x):
			started = True
		if started:
			yield x

@I.lift  
def skip(n: int, xs: Iterable[A]) -> Iterable[A]:
	"""`skip(n, [x1, ..., xn, *xs]) = xs`"""
	return itertools.islice(xs, n, None)