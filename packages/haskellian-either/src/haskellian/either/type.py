from typing import Generic, TypeVar, Literal, Callable
from abc import ABC
from dataclasses import dataclass

A = TypeVar('A')
L = TypeVar('L', covariant=True)
R = TypeVar('R', covariant=True)
L2 = TypeVar('L2')
R2 = TypeVar('R2')

@dataclass
class Either(ABC, Generic[L, R]):
  value: L | R
  tag: Literal['left', 'right']

  def match(self, on_left: Callable[[L], A], on_right: Callable[[R], A]) -> A:
    """Unwrap an `Either` by matching both branches"""
    match self:
      case Left(err):
        return on_left(err)
      case Right(value):
        return on_right(value)
      
  def match_(self, on_left: Callable[[], A], on_right: Callable[[], A]) -> A:
    """Like `match`, but handlers don't get the wrapped value"""
    return self.match(lambda _: on_left(), lambda _: on_right())
  
  def tap(self, on_left: Callable[[L], None] = lambda _: None, on_right: Callable[[R], None] = lambda _: None) -> 'Either[L, R]':
    """Execute `on_left`/`on_right` but return the either as is"""
    match self:
      case Left(err):
        on_left(err)
      case Right(value):
        on_right(value)
    return self
  
  def mapl(self, f: Callable[[L], L2]) -> 'Either[L2, R]':
    """Map the left branch"""
    return self.match(lambda x: Left(f(x)), Right)
  
  def fmap(self, f: Callable[[R], R2]) -> 'Either[L, R2]':
    return self.match(Left, lambda x: Right(f(x)))
  
  __or__ = fmap
  """Alias of `fmap`"""
      
  def bind(self, f: 'Callable[[R], Either[L2, R2]]') -> 'Either[L|L2, R2]':
    return self.match(Left, f)
  
  __and__ = bind
  """Alias of `bind`"""

  def unsafe(self) -> R:
    """Unwraps the value or throws the left exception"""
    match self:
      case Left(err):
        exc = err if isinstance(err, BaseException) else Exception(err)
        raise exc
      case Right(value):
        return value
  
  def expect(self, exc: Callable[[], BaseException]) -> R:
    """Unwraps the value or throws the exception"""
    match self:
      case Left():
        raise exc()
      case Right(value):
        return value

@dataclass
class Left(Either[L, R], Generic[L, R]):
  value: L = None
  tag: Literal['left'] = 'left'

@dataclass
class Right(Either[L, R], Generic[L, R]):
  value: R = None
  tag: Literal['right'] = 'right'