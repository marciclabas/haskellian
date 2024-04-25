from haskellian import DEBUG_IMPORTS
if DEBUG_IMPORTS:
  print('Import:', __name__)
from dataclasses import dataclass
from typing_extensions import TypeVar, Callable, Generic
from haskellian import Monad

A = TypeVar('A')
B = TypeVar('B')


@dataclass
class Pipe(Monad[A], Generic[A]):
  """The simplest monad: just a value. But one that can be easily operated on:
  
  ```
  (Pipe('world hello')
  .f(str.title)
  .f(lambda s: s.split(' '))
  .f(sorted)
  .f(', '.join)
  ).value
  # 'Hello, World'
  ```
  """

  value: A

  def bind(self, f: Callable[[A], 'Pipe[B]']) -> 'Pipe[B]':
    return f(self.value)
  
  def f(self, f: Callable[[A], B]) -> 'Pipe[B]':
    return self.fmap(f) # type: ignore
  
  @classmethod
  def of(cls, value: A) -> 'Pipe[A]':
    return cls(value)