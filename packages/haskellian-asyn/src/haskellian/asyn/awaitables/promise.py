from typing import TypeVar, Generic, Callable, Awaitable
from .ops import then, bind

T = TypeVar('T')
U = TypeVar('U')

class Promise(Generic[T], Awaitable[T]):
  def __init__(self, x: Awaitable[T]):
    self.x = x

  def __await__(self):
    return self.x.__await__()
  
  def then(self, f: Callable[[T], U]) -> 'Promise[U]':
    return Promise(then(f, self))

  __or__ = then

  def bind(self, f: Callable[[T], Awaitable[U]]) -> 'Promise[U]':
    return Promise(bind(f, self))
  
  __and__ = bind