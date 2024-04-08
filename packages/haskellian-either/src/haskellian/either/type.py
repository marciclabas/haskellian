from typing import Generic, TypeVar, Literal, Callable, Any, TypeGuard
from abc import ABC, abstractmethod
from dataclasses import dataclass

A = TypeVar('A')
L = TypeVar('L', covariant=True)
R = TypeVar('R', covariant=True)
L2 = TypeVar('L2')
R2 = TypeVar('R2')

@dataclass(eq=False)
class IsLeft(BaseException, Generic[L]):
  value: L

class EitherBase(ABC, Generic[L, R]):

  @abstractmethod
  def match(self, on_left: Callable[[L], A], on_right: Callable[[R], A]) -> A:
    """Unwrap an `Either` by matching both branches"""

  @abstractmethod
  def unsafe(self) -> R:
    """Unwraps the value or throws an `IsLeft` exception
    
    (`IsLeft.value` will contain the wrapped value)"""
    

  def bind(self, f: 'Callable[[R], Either[L, R2]]') -> 'Either[L, R2]':
    return self.match(lambda x: Left(x), f)

  def fmap(self, f: Callable[[R], R2]) -> 'Either[L, R2]':
    return self.match(lambda x: Left(x), lambda x: Right(f(x)))

  def mapl(self, f: Callable[[L], L2]) -> 'Either[L2, R]':
    """Map the left branch"""
    return self.match(lambda x: Left(f(x)), lambda x: Right(x))

  __or__ = fmap
  """Alias of `fmap`"""
  
  __and__ = bind
  """Alias of `bind`"""
  
  def match_(self, on_left: Callable[[], A], on_right: Callable[[], A]) -> A:
    """Like `match`, but handlers don't get the wrapped value"""
    return self.match(lambda _: on_left(), lambda _: on_right())
  
@dataclass
class Left(EitherBase[L, Any], Generic[L]):
  value: L
  tag: Literal['left'] = 'left'

  def match(self, on_left: Callable[[L], A], on_right: Callable[[R], A]) -> A:
    return on_left(self.value)
  
  def unsafe(self):
    raise IsLeft(self.value)

@dataclass
class Right(EitherBase[Any, R], Generic[R]):
  value: R
  tag: Literal['right'] = 'right'

  def match(self, on_left: Callable[[L], A], on_right: Callable[[R], A]) -> A:
    return on_right(self.value)
  
  def unsafe(self) -> R:
    return self.value

Either = Left[L] | Right[R]