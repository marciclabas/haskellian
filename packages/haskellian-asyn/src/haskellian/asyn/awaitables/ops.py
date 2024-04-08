from typing import TypeVar, Callable, Awaitable
import asyncio
T = TypeVar('T')
U = TypeVar('U')

async def then(f: Callable[[T], U], x: Awaitable[T]) -> U:
  return f(await x)

async def bind(f: Callable[[T], Awaitable[U]], x: Awaitable[T]) -> U:
  return await f(await x)

async def of(x: T) -> T:
  return T

async def all(xs: list[Awaitable[T]]) -> list[T]:
  return asyncio.gather(*xs)