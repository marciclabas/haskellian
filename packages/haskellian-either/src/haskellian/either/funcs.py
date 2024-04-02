from typing import Callable, TypeVar
from ramda import curry
from .type import Either, Left, Right

A = TypeVar('A')
R = TypeVar('R')
R2 = TypeVar('R2')
L = TypeVar('L')
L2 = TypeVar('L2')

def safe(func: Callable[[], R]) -> Either[Exception, R]:
  try:
    return Right(func())
  except Exception as e:
    return Left(e)
  
def unsafe(either: Either[Exception, R]) -> R:
  """Unwraps the value or throws the left exception"""
  match either:
    case Left(exc):
      raise exc
    case Right(value):
      return value
    
@curry
def match(on_left: Callable[[L], A], on_right: Callable[[R], A], x: Either[L, R]) -> A:
  """Unwrap an `Either` by matching both branches"""
  match x:
    case Left(err):
      return on_left(err)
    case Right(value):
      return on_right(value)
    
@curry
def fmap(f: Callable[[R], R2], x: Either[L, R]) -> Either[L, R2]:
  return match(Left, lambda x: Right(f(x)), x)
    
@curry
def bind(f: Callable[[R], Either[L2, R2]], x: Either[L, R]) -> Either[L|L2, R2]:
  return match(Left, f, x)