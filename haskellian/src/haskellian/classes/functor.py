from typing_extensions import Callable, Generic, TypeVar
from abc import ABC, abstractmethod

A = TypeVar('A', covariant=True)
B = TypeVar('B')

class Functor(ABC, Generic[A]):
  @abstractmethod
  def fmap(self, f: Callable[[A], B]) -> 'Functor[B]':
    ...

  def __or__(self, f: Callable[[A], B]) -> 'Functor[B]':
    return self.fmap(f)
