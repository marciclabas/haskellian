from haskellian import DEBUG_IMPORTS, asyn_iter as AI, promise as P
if DEBUG_IMPORTS:
  print('Import:', __name__)
from typing_extensions import TypeVar, Generic, AsyncIterator

A = TypeVar('A')
B = TypeVar('B')

class ManagedAsync(AI.AsyncIter[A], Generic[A]):

  def __init__(self):
    self.xs: list[A] = []
    self._next = P.ManagedPromise()
    self.ended: bool = False

  def push(self, value: A):
    self.xs.append(value)
    if not self._next.resolved:
      self._next.resolve()

  def end(self):
    self.ended = True
    if not self._next.resolved:
      self._next.resolve()

  def __aiter__(self) -> AsyncIterator[A]:
    return self

  async def __anext__(self) -> A:
    if len(self.xs) > 0:
      return self.xs.pop(0)
    elif self.ended:
      raise StopAsyncIteration()
    else:
      await self._next
      self._next = P.ManagedPromise()
      return await self.__anext__()