from typing import TypeVar, AsyncIterable
import asyncio


class Guard: ...
A = TypeVar('A')
Queue = asyncio.Queue[Guard|A]

async def iterate(q: asyncio.Queue[A | Guard]) -> AsyncIterable[A]:
    """Iterate a queue `q` until `Guard` is popped (awaits indefinetely otherwise)"""
    while True:
        match await q.get():
            case Guard(): return
            case x: yield x