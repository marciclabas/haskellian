from typing_extensions import TypeVar, Callable, Iterable, overload
from .either import Either, Left, Right

A = TypeVar('A')
R = TypeVar('R')
L = TypeVar('L')
Err = TypeVar('Err', bound=Exception)

def safe(func: Callable[[], R], Exc: type[Err] = Exception) -> 'Either[Err, R]':
    try:
      return Right(func())
    except Exc as e:
      return Left(e)
    
def maybe(x: R | None) -> 'Either[None, R]':
  return Left(None) if x is None else Right(x)

@overload
def get_or(default: R) -> Callable[[Either[L, R]], R]: ...
@overload
def get_or(default: A) -> Callable[[Either[L, R]], R | A]: ...
def get_or(default: A) -> Callable[[Either[L, R]], R | A]:
  return lambda e: e.get_or(default)

def unsafe(x: Either[L, R]) -> R:
  return x.unsafe()
    
def sequence(eithers: Iterable[Either[L, R]]) -> Either[list[L], list[R]]:
  """List of lefts if any (thus with length in `[1, len(eithers)]`), otherwise list of all rights (with length `len(eithers)`)"""
  lefts: list[L] = []
  rights: list[R] = []
  for x in eithers:
    x.match(lefts.append, rights.append)
  return Right(rights) if lefts == [] else Left(lefts)

def filter(eithers: Iterable[Either[L, R]]) -> Iterable[R]:
  for e in eithers:
    match e:
      case Right(value):
        yield value

def filter_lefts(eithers: Iterable[Either[L, R]]) -> Iterable[L]:
  for e in eithers:
    match e:
      case Left(err):
        yield err

def take_while(eithers: Iterable[Either[L, R]]) -> Iterable[R]:
  for e in eithers:
    match e:
      case Right(x):
        yield x
      case _:
        return