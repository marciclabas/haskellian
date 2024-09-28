from typing_extensions import Callable, Generic, TypeVar
from abc import ABC, abstractmethod
from .applicative import Applicative

A = TypeVar('A', covariant=True)
B = TypeVar('B')


class Monad(Applicative[A], ABC, Generic[A]):
  
  @classmethod
  @abstractmethod
  def of(cls, value: B) -> 'Monad[B]':
    ...

  @abstractmethod
  def bind(self, f: Callable[[A], 'Monad[B]']) -> 'Monad[B]':
    ...

  def ap(self, f: 'Monad[Callable[[A], B]]') -> 'Monad[B]': # type: ignore
    return f.bind(lambda func: self.bind(lambda x: self.of(func(x))))
  
  def fmap(self, f: Callable[[A], B]) -> 'Monad[B]':
    def lifted(a: A):
      b = f(a)
      return self.of(b)
    return self.bind(lifted)

  @classmethod
  def pure(cls, value: B) -> 'Monad[B]':
    return cls.of(value)