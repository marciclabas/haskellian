from haskellian import promise as P
from typing_extensions import TypeVar, Generic
import asyncio

A = TypeVar('A', covariant=True)
B = TypeVar('B')

class ManagedPromise(P.Promise[A], Generic[A]):
  """Managed awaitable"""
  
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
  