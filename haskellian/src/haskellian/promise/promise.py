from haskellian import Monad, promise as P
from typing_extensions import TypeVar, Generic, Callable, Awaitable

A = TypeVar('A', covariant=True)
B = TypeVar('B')

class Promise(Monad[A], Generic[A], Awaitable[A]):

  def __repr__(self) -> str:
    return 'Promise()'
  
  def __init__(self, x: Awaitable[A]):
    self.x = x

  def __await__(self):
    return self.x.__await__()
  
  @classmethod
  def of(cls, x: B) -> 'Promise[B]': # type: ignore
    return Promise(P.of(x))
  
  def then(self, f: Callable[[A], B]) -> 'Promise[B]':
    """Alias for `fmap`"""
    return Promise(P.then(f, self))
  
  def bind(self, f: Callable[[A], Awaitable[B]]) -> 'Promise[B]': # type: ignore
    return Promise(P.bind(f, self))
  
  def fmap(self, f: Callable[[A], B]) -> 'Promise[B]':
    return self.then(f)
  
  def __or__(self, f: Callable[[A], B]) -> 'Promise[B]':
    return self.then(f)

  
  def __and__(self, f: Callable[[A], Awaitable[B]]) -> 'Promise[B]':
    return self.bind(f)
  
  async def run(self) -> A:
    return await self