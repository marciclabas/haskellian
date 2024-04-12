from typing import Callable, Generic, TypeVar, Awaitable, AsyncIterator, AsyncIterable, TypeGuard, overload, TypeVarTuple
from .. import ops

A = TypeVar('A')
B = TypeVar('B')
As = TypeVarTuple('As')

class AsyncIter(Generic[A], AsyncIterator[A]):

  def __init__(self, xs: AsyncIterable[A]):
    self._xs = xs

  async def __anext__(self) -> A:
    async for x in self._xs:
      return x
    raise StopAsyncIteration()
  
  def map(self, f: Callable[[A], B]) -> 'AsyncIter[B]':
    return AsyncIter(ops.map(f, self))
  
  __or__ = map
  
  def amap(self, f: Callable[[A], Awaitable[B]]) -> 'AsyncIter[B]':
    return AsyncIter(ops.amap(f, self))
  
  def flatmap(self, f: Callable[[A], AsyncIterable[B]]) -> 'AsyncIter[B]':
    return AsyncIter(ops.flatmap(f, self))
  
  __and__ = flatmap

  @overload
  def filter(self, p: Callable[[A], TypeGuard[B]]) -> 'AsyncIter[B]': ...
  @overload
  def filter(self, p: Callable[[A], bool]) -> 'AsyncIter[A]': ...
  def filter(self, p: Callable[[A], bool]) -> 'AsyncIter[A]':
    return AsyncIter(ops.filter(p, self))

  async def sync(self) -> list[A]:
    return await ops.syncify(self)
  
  def skip(self, n: int) -> 'AsyncIter[A]':
    return AsyncIter(ops.skip(n, self))
  
  async def head(self) -> A | None:
    async for x in self._xs:
      return x
  
  def batch(self, n: int) -> 'AsyncIter[tuple[A, ...]]':
    return AsyncIter(ops.batch(n, self))
  
  def enumerate(self) -> 'AsyncIter[tuple[int, A]]':
    return AsyncIter(ops.enumerate(self))
  
  async def split(self, n: int) -> tuple[list[A], 'AsyncIter[A]']:
    head, xs = await ops.split(n, self)
    return head, AsyncIter(xs)
  
  def prefetch(self, n: int) -> 'AsyncIter[A]':
    return AsyncIter(ops.prefetched(n, self))