import asyncio
from typing import AsyncIterable, Callable, TypeVar, Iterable
import ramda as R

A = TypeVar("A")
B = TypeVar("B")

@R.curry
async def map(f: Callable[[A], B], xs: AsyncIterable[A]) -> AsyncIterable[B]:
    async for x in xs:
        yield f(x)
        
async def flatten(xxs: AsyncIterable[Iterable[A]]) -> AsyncIterable[A]:
    async for xs in xxs:
        for x in xs:
            yield x 

async def enumerate(xs: AsyncIterable[A]) -> AsyncIterable[tuple[int, A]]:
    i = 0
    async for x in xs:
        yield i, x
        i += 1
        
async def asyncify(xs: Iterable[A]) -> AsyncIterable[A]:
    for x in xs:
        yield x
        
async def syncify(xs: AsyncIterable[A]) -> list[A]:
    ys = []
    async for x in xs:
        ys += [x]
    return ys
