from typing import TypeVar, AsyncIterable
import asyncio
from .. import either

class Guard: ...
A = TypeVar('A')
Queue = asyncio.Queue[Guard|A]

async def iterate(q: asyncio.Queue[A | Guard]) -> AsyncIterable[A]:
    """Iterate a queue `q` until `Guard` is popped (awaits indefinetely otherwise)"""
    while True:
        match await q.get():
            case Guard(): return
            case x: yield x
            
def enqueue(xs: AsyncIterable[A], guard: bool = False) -> asyncio.Queue[A]:
    """Enqueue `xs` into the returned queue. Optionally, add `Guard` at the end"""
    q = asyncio.Queue()
    async def f():
        async for x in xs:
            q.put_nowait(x)
        if guard:
            q.put_nowait(Guard())
    asyncio.Task(f())
    return q
    
def pop_all(q: asyncio.Queue[A]) -> list[A]:
    """Synchronously return all elements of the queue"""
    xs = []
    while not isinstance((x := either(q.get_nowait)), asyncio.QueueEmpty):
        xs += [x]
    return xs