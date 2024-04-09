from typing import Generic, TypeVar, Literal, Callable, Any, TypeGuard
from abc import ABC, abstractmethod
from dataclasses import dataclass

A = TypeVar('A', covariant=True)
L = TypeVar('L', covariant=True)
R = TypeVar('R', covariant=True)
L2 = TypeVar('L2')
R2 = TypeVar('R2')

@dataclass(eq=False)
class IsLeft(BaseException, Generic[L]):
  value: L

class EitherBase(ABC, Generic[L, R]):

  @abstractmethod
  def _match(self, on_left: Callable[[L], A], on_right: Callable[[R], A]) -> int:
    """Unwrap an `Either` by matching both branches"""
  
  def match(self, on_left: Callable[[L], A], on_right: Callable[[R], A]) -> A:
    """Unwrap an `Either` by matching both branches"""
    return self._match(on_left, on_right)

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
class Left(EitherBase[L, R], Generic[L, R]):
  value: L = None
  tag: Literal['left'] = 'left'

  def _match(self, on_left, on_right):
    return on_left(self.value)
  
  def unsafe(self):
    raise IsLeft(self.value)

@dataclass
class Right(EitherBase[L, R], Generic[L, R]):
  value: R = None
  tag: Literal['right'] = 'right'

  def _match(self, on_left, on_right):
    return on_right(self.value)
  
  def unsafe(self) -> R:
    return self.value

Either = Left[L, R] | Right[L, R]