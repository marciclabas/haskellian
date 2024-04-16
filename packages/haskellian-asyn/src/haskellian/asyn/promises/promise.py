from typing import TypeVar, Generic, Callable, Awaitable

T = TypeVar('T')
U = TypeVar('U')

async def then(f: Callable[[T], U], x: Awaitable[T]) -> U:
  return f(await x)

async def bind(f: Callable[[T], Awaitable[U]], x: Awaitable[T]) -> U:
  return await f(await x)

class Promise(Generic[T], Awaitable[T]):
  def __init__(self, x: Awaitable[T]):
    self.x = x

  def __await__(self):
    return self.x.__await__()
  
  def then(self, f: Callable[[T], U]) -> 'Promise[U]':
    """Your usual functor map"""
    return Promise(then(f, self))

  __or__ = then

  def bind(self, f: Callable[[T], Awaitable[U]]) -> 'Promise[U]':
    return Promise(bind(f, self))
  
  __and__ = bind

  async def run(self) -> T:
    return await self