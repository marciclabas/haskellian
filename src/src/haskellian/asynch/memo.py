from typing import AsyncIterable, Awaitable, TypeVar, Generic

A = TypeVar("A")

class AsyncMemo(Generic[A]):
    def __init__(self, xs: AsyncIterable[A]):
        self.xs = xs
        self.stored = []
    
    def __aiter__(self):
        return self
    
    async def __anext__(self) -> Awaitable[A]:
        x = await self.xs.__anext__()
        self.stored += [x]
        return x
    
    async def all(self) -> AsyncIterable[A]:
        for x in self.stored:
            yield x
        async for x in self.xs:
            self.stored += [x]
            yield x