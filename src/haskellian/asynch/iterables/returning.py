from typing import Awaitable, TypeVar, TypeVarTuple, Callable, Protocol, Generic, AsyncGenerator, AsyncIterator, Any
import asyncio


Yield = TypeVar('Yield')
Send = TypeVar('Send')
Return = TypeVar('Return')
T = TypeVar('T')

Callback = Callable[[T], None]
Args = TypeVarTuple('Args')

class ReturnableCPS(Protocol, Generic[Yield, Send, Return]):
  def __call__(ret: Callback[Return], *args: *Args, **kwargs) -> AsyncGenerator[Yield, Send]:
    ...
    
class ReturnedAsyncIter(AsyncGenerator[Yield, Send], Generic[Yield, Send, Return]):
  def __init__(self, xs: AsyncGenerator[Yield, Send], ret: asyncio.Future):
    self._xs = xs
    self.ret = ret
  
  def __aiter__(self) -> AsyncIterator[Yield]:
    return self._xs.__aiter__()
  
  def __anext__(self) -> Awaitable[Yield]:
    return self._xs.__anext__()
  
  def asend(self, value: Send) -> Awaitable[Yield]:
    return self._xs.asend(value)
  
  def athrow(self, *args, **kwargs):
    return self._xs.athrow(*args, **kwargs)
  
def returned(func: Callable[[*Args], AsyncGenerator[Yield, Send]]):
  retval = asyncio.Future()
  
  def _f(*args: *Args, **kwargs) -> ReturnedAsyncIter[Yield, Send, Return]:
    return ReturnedAsyncIter(
      xs=(x async for x in func(retval.set_result, *args, **kwargs)),
      ret=retval
    )
  return _f