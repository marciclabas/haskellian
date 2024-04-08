from typing import TypeVar, TypeGuard, Any
from .type import Either, Left, Right

L = TypeVar('L')
R = TypeVar('R')

def is_left(either: Either[L, R]) -> TypeGuard[Left[L]]:
  return either.tag == 'left'

def is_right(either: Either[L, R]) -> TypeGuard[Right[R]]:
  return either.tag == 'right'