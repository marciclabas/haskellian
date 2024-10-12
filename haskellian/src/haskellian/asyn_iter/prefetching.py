from haskellian import asyn_iter as AI
from typing_extensions import TypeVar, AsyncIterable
import asyncio

A = TypeVar('A')

@AI.lift
def prefetched(prefetch: int, xs: AsyncIterable[A]) -> AsyncIterable[A]:
  """Prefetch `prefetch` elements from `xs`
  - If `prefetched < 1`, it'll be clipped to `1`
  """
  buffer = asyncio.Queue(maxsize=max(prefetch, 1))
  sentinel = object()

  async def producer():
    async for x in xs:
      await buffer.put(x)
    await buffer.put(sentinel)

  async def consumer():
    while True:
      item = await buffer.get()
      if item is sentinel:
        break
      yield item

  asyncio.create_task(producer())
  return consumer()