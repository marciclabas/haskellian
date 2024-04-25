from haskellian import DEBUG_IMPORTS, asyn_iter as AI
if DEBUG_IMPORTS:
  print('Import:', __name__)
from typing_extensions import TypeVar, AsyncIterable
import asyncio

A = TypeVar('A')

@AI.lift
def prefetched(prefetch: int, xs: AsyncIterable[A]) -> AsyncIterable[A]:
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