import asyncio
from typing import Callable, Awaitable, TypeVar
import ramda as R

A = TypeVar("A")
B = TypeVar("B")

async def either(x: Awaitable[A]) -> A | Exception:
    try:
        return await x
    except Exception as e:
        return e
    
async def uneither(x: Awaitable[A] | Exception) -> Awaitable[A]:
    match (await x):
        case Exception(e):
            raise e
        case v:
            return v
    
async def safe(x: Awaitable[A]) -> A | None:
    try:
        return await x
    except:
        return None
    
    
async def wrap(x: A) -> Awaitable[A]:
    return x
    
async def then(f: Callable[[A], B], x: Awaitable[A]) -> Awaitable[B]:
    return f(await x)

async def bind(f: Callable[[A], Awaitable[B]], x: Awaitable[A]) -> Awaitable[B]:
    return await f(await x)