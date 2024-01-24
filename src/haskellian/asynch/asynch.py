import asyncio
import inspect
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
        case Exception() as e:
            raise e
        case v:
            return v
    
async def safe(x: Awaitable[A]) -> A | None:
    try:
        return await x
    except:
        return None
    
    
async def wrap(x: A) -> Awaitable[A]:
    """aka `return` for the `Future` monad"""
    return x

async def wait(x: A | Awaitable[A]) -> Awaitable[A]:
    return (await x) if inspect.isawaitable(x) else x
    
@R.curry
async def then(f: Callable[[A], B], x: Awaitable[A]) -> Awaitable[B]:
    """aka `fmap` aka `<$>` for the `Future` monad"""
    return f(await x)

@R.curry
async def bind(f: Callable[[A], Awaitable[B]], x: Awaitable[A]) -> Awaitable[B]:
    """aka `flatmap` aka `chain` aka `>>=` for the `Future` monad"""
    return await f(await x)