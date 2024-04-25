from haskellian import DEBUG_IMPORTS
if DEBUG_IMPORTS:
  print('Import:', __name__)
from dataclasses import dataclass
from typing_extensions import TypeVar, Callable, Generic
from haskellian import Monad

A = TypeVar('A')
B = TypeVar('B')

@dataclass
class Thunk(Monad[A], Generic[A]):

  supplier: Callable[[], A]

  def fmap(self, f: Callable[[A], B]) -> 'Thunk[B]':
    return Thunk(lambda: f(self.supplier()))
  
  def bind(self, f: Callable[[A], 'Thunk[B]']) -> 'Thunk[B]':
    def _supplier():
      value = self.get()
      thunk = f(value)
      value2 = thunk.get()
      return value2
    return Thunk(_supplier)
  
  def ap(self, f: 'Thunk[Callable[[A], B]]') -> 'Thunk[B]':
    return super().ap(f) # type: ignore

  def __or__(self, f: Callable[[A], B]) -> 'Thunk[B]':
    return self.fmap(f)
  
  def get(self) -> A:
    return self.supplier()
  
  @classmethod
  def of(cls, value: A) -> 'Thunk[A]':
    return cls(lambda: value)