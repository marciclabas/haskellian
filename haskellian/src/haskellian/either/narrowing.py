from haskellian import DEBUG_IMPORTS
if DEBUG_IMPORTS:
  print('Import:', __name__)
from typing_extensions import TypeVar, TypeGuard
from .either import Either, Left, Right

L = TypeVar('L')
R = TypeVar('R')

def is_left(either: Either[L, R]) -> TypeGuard[Left[L, R]]:
  return either.tag == 'left'

def is_right(either: Either[L, R]) -> TypeGuard[Right[L, R]]:
  return either.tag == 'right'