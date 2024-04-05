from typing import TypeVar, Callable, Iterable
from .type import Either, Left, Right

R = TypeVar('R')
L = TypeVar('L')
Err = TypeVar('Err', bound=Exception)

def safe(func: Callable[[], R], Exc: type[Err] = Exception) -> 'Either[Err, R]':
    try:
      return Right(func())
    except Exc as e:
      return Left(e)
    
def maybe(x: R | None) -> 'Either[None, R]':
  return Left() if x is None else Right(x)
    
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
