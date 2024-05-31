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
  value: A | None = None

  def fmap(self, f: Callable[[A], B]) -> 'Thunk[B]':
    return Thunk(lambda: f(self()))
  
  def bind(self, f: Callable[[A], 'Thunk[B]']) -> 'Thunk[B]':
    def _supplier():
      value = self()
      thunk = f(value)
      value2 = thunk()
      return value2
    return Thunk(_supplier)
  
  def ap(self, f: 'Thunk[Callable[[A], B]]') -> 'Thunk[B]':
    return super().ap(f) # type: ignore

  def __or__(self, f: Callable[[A], B]) -> 'Thunk[B]':
    return self.fmap(f)
  
  def __call__(self) -> A:
    if self.value is None:
      self.value = self.supplier()
    return self.value
  
  @classmethod
  def of(cls, value: A) -> 'Thunk[A]':
    return cls(lambda: value)