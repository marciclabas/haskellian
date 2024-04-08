from typing import TypeVar, Generic, AsyncIterator
from ..awaitables import ManagedAwaitable
T = TypeVar('T')
U = TypeVar('U')

class ManagedIterable(Generic[T], AsyncIterator[T]):

  def __init__(self):
    self.xs: list[T] = []
    self._next = ManagedAwaitable()
    self.ended: bool = False

  def push(self, value: T):
    self.xs.append(value)
    if not self._next.resolved:
      self._next.resolve()

  def end(self):
    self.ended = True
    if not self._next.resolved:
      self._next.resolve()

  async def __anext__(self) -> T:
    if len(self.xs) > 0:
      return self.xs.pop(0)
    elif self.ended:
      raise StopAsyncIteration()
    else:
      await self._next
      self._next = ManagedAwaitable()
      return await self.__anext__()