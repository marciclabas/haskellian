from typing import TypeVar, Generic, Awaitable, Callable
import asyncio
from haskellian import promise as P

A = TypeVar('A', covariant=True)
B = TypeVar('B')

class ManagedPromise(P.Promise[A], Generic[A], Awaitable[A]):
  
  value: A

  def __init__(self):
    self.resolved = False
    self.event = asyncio.Event()

  def resolve(self, value: A = None): # type: ignore
    self.value = value
    self.resolved = True
    self.event.set()

  def __await__(self):
    async def wait():
      await self.event.wait()
      return self.value
    return wait().__await__()
  