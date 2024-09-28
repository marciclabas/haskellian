from typing_extensions import Callable, Generic, TypeVar
from abc import ABC, abstractmethod
from .functor import Functor

A = TypeVar('A', covariant=True)
B = TypeVar('B')

class Applicative(Functor[A], ABC, Generic[A]):
  
  @classmethod
  @abstractmethod
  def pure(cls, value: B) -> 'Applicative[B]':
    ...

  @abstractmethod
  def ap(self, f: 'Applicative[Callable[[A], B]]') -> 'Applicative[B]':
    ...

  def fmap(self, f: Callable[[A], B]) -> 'Applicative[B]':
    return self.ap(self.pure(f))
