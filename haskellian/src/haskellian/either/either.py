from haskellian import DEBUG_IMPORTS
if DEBUG_IMPORTS:
  print('Import:', __name__)
from typing_extensions import Generic, TypeVar, Literal, Callable, Any, overload
from dataclasses import dataclass
from abc import ABC, abstractmethod
from haskellian import Monad

A = TypeVar('A')
L = TypeVar('L', covariant=True)
R = TypeVar('R', covariant=True)
L2 = TypeVar('L2')
R2 = TypeVar('R2')

@dataclass(eq=False)
class IsLeft(BaseException, Generic[L]):
  value: L

class EitherBase(Monad[R], ABC, Generic[L, R]):

  @abstractmethod
  def _match(self, on_left: Callable[[L], A], on_right: Callable[[R], A]) -> A:
    """Unwrap an `Either` by matching both branches"""
  
  def match(self, on_left: Callable[[L], A], on_right: Callable[[R], A]) -> A:
    """Unwrap an `Either` by matching both branches"""
    return self._match(on_left, on_right)

  @abstractmethod
  def unsafe(self) -> R:
    """Unwraps the value or throws an `IsLeft` exception
    
    (`IsLeft.value` will contain the wrapped value)"""

  def expect(self, error_msg) -> R:
    """Unwraps the value or throws `IsLeft(error_msg)` exception"""
    return self.mapl(lambda _: error_msg).unsafe()
    
  @classmethod
  def of(cls, x: A) -> 'Right[Any, A]':
    return Right(x)

  def bind(self, f: 'Callable[[R], Either[L2, R2]]') -> 'Either[L|L2, R2]':
    return self.match(lambda x: Left(x), f)

  def fmap(self, f: Callable[[R], R2]) -> 'Either[L, R2]':
    return super().fmap(f) # type: ignore

  def mapl(self, f: Callable[[L], L2]) -> 'Either[L2, R]':
    """Map the left branch"""
    return self.match(lambda x: Left(f(x)), lambda x: Right(x))
  
  @overload
  def get_or(self, fallback: R) -> R: ... # type: ignore
  @overload
  def get_or(self, fallback: A) -> A | R: ...
  def get_or(self, fallback): # type: ignore
    return self.match(lambda _: fallback, lambda x: x)

  def ap(self, f: 'Either[L, Callable[[R], R2]]') -> 'Either[L, R2]':
    return super().ap(f) # type: ignore
  
  def __or__(self, f: Callable[[R], R2]) -> 'Either[L, R2]':
    return self.fmap(f)
  
  def match_(self, on_left: Callable[[], A], on_right: Callable[[], A]) -> A:
    """Like `match`, but handlers don't get the wrapped value"""
    return self.match(lambda _: on_left(), lambda _: on_right())
  
@dataclass
class Left(EitherBase[L, R], Generic[L, R]):
  value: L = None # type: ignore
  tag: Literal['left'] = 'left'

  def _match(self, on_left, on_right):
    return on_left(self.value)
  
  def unsafe(self):
    raise IsLeft(self.value)

@dataclass
class Right(EitherBase[L, R], Generic[L, R]):
  value: R = None # type: ignore
  tag: Literal['right'] = 'right'

  def _match(self, on_left, on_right):
    return on_right(self.value)
  
  def unsafe(self) -> R:
    return self.value

Either = Left[L, R] | Right[L, R]