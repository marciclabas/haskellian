import asyncio
from typing import Awaitable, TypeVar
import ramda as R

A = TypeVar("A")
B = TypeVar("B")

async def either(x: Awaitable[A]) -> A | Exception:
    try:
        return await x
    except Exception as e:
        return e
    
async def safe(x: Awaitable[A]) -> A | None:
    try:
        return await x
    except:
        return None
    
async def wrap(x: A) -> Awaitable[A]:
    return x
    