from typing import Generic, Awaitable, TypeVar
import asyncio
from .asynch import then

T = TypeVar('T')

class ManagedAsync(Generic[T]):
  """Like a `Future` but lean"""
  def __init__(self):
    self.value = None
    self.event = asyncio.Event()
  
  def resolve(self, value: T = None):
    self.value = value
    self.event.set()
  
  def wait(self) -> Awaitable[T]:
    return then(lambda _: self.value, self.event.wait())