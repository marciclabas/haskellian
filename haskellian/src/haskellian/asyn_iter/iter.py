from haskellian import asyn_iter as AI, Monad
from typing_extensions import Callable, Generic, TypeVar, Awaitable, AsyncIterator, AsyncIterable, TypeGuard, overload, TypeVarTuple

A = TypeVar('A', covariant=True)
B = TypeVar('B')
As = TypeVarTuple('As')

class AsyncIter(Monad[A], Generic[A], AsyncIterator[A]):

  def __repr__(self):
    return f'AsyncIter({self._xs})'

  def __init__(self, xs: AsyncIterable[A]):
    self._xs = xs

  @classmethod
  def of(cls, value: B) -> 'AsyncIter[B]':
    return AsyncIter(AI.asyncify([value]))

  async def __anext__(self) -> A:
    async for x in self._xs:
      return x
    raise StopAsyncIteration()
  
  def map(self, f: Callable[[A], B]) -> 'AsyncIter[B]':
    return AI.map(f, self)
  
  __or__ = map
  
  def amap(self, f: Callable[[A], Awaitable[B]]) -> 'AsyncIter[B]':
    return AI.amap(f, self)
  
  def bind(self, f: Callable[[A], AsyncIterable[B]]) -> 'AsyncIter[B]': # type: ignore
    return AI.flatmap(f, self)
  
  def flatmap(self, f: Callable[[A], AsyncIterable[B]]) -> 'AsyncIter[B]':
    """Alias of `bind`"""
    return self.bind(f)
  
  def __and__(self, f: Callable[[A], AsyncIterable[B]]) -> 'AsyncIter[B]':
    """Alias of `bind`"""
    return self.bind(f)
  
  @overload
  def filter(self, p: Callable[[A], TypeGuard[B]]) -> 'AsyncIter[B]': ...
  @overload
  def filter(self, p: Callable[[A], bool]) -> 'AsyncIter[A]': ...
  def filter(self, p): # type: ignore
    return AI.filter(p, self)

  async def sync(self) -> list[A]:
    return await AI.syncify(self)
  
  async def head(self) -> A | None:
    return await AI.head(self)
    
  def take(self, n: int) -> 'AsyncIter[A]':
    return AI.take(n, self)
  
  def skip(self, n: int) -> 'AsyncIter[A]':
    return AI.skip(n, self)
  
  def every(self, n: int) -> 'AsyncIter[A]':
    return AI.every(n, self)
  
  def batch(self, n: int) -> 'AsyncIter[tuple[A, ...]]':
    return AI.batch(n, self)
  
  def enumerate(self) -> 'AsyncIter[tuple[int, A]]':
    return AI.enumerate(self)
  
  async def split(self, n: int) -> tuple[list[A], 'AsyncIter[A]']:
    head, xs = await AI.split(n, self)
    return head, AsyncIter(xs)
  
  def prefetch(self, n: int) -> 'AsyncIter[A]':
    return AI.prefetched(n, self) if n > 0 else self


  def i(self, f: Callable[['AsyncIter[A]'], AsyncIterable[B]]) -> 'AsyncIter[B]':
    """Apply an arbitrary iterable function"""
    return AsyncIter(f(self))
  