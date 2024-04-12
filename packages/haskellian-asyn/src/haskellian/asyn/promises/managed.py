from typing import TypeVar, Generic, Awaitable
import asyncio

T = TypeVar('T')

class ManagedAwaitable(Generic[T], Awaitable[T]):
  
  value: T

  def __init__(self):
    self.resolved = False
    self.event = asyncio.Event()

  def resolve(self, value: T = None): # type: ignore
    self.value = value
    self.resolved = True
    self.event.set()

  def __await__(self):
    async def wait():
      await self.event.wait()
      return self.value
    return wait().__await__()