from typing import TypeVar, Callable, Awaitable, Mapping, Iterable, overload
from inspect import isawaitable
from haskellian.iterables import unzip
import asyncio
from haskellian.asyn.promises.funcs import lift

T = TypeVar('T')
U = TypeVar('U')

@lift
async def of(x: T) -> T:
  return x

@lift
async def wait(x: T | Awaitable[T]) -> T:
  return await x if isawaitable(x) else x

@overload
async def all(xs: Iterable[Awaitable[T]]) -> list[T]: ...
@overload
async def all(xs: Mapping[str, Awaitable[T]]) -> dict[str, T]: ...

async def all(xs):
  if isinstance(xs, Mapping):
    keys, values = unzip(xs.items())
    results = await asyncio.gather(*values)
    return dict(zip(keys, results))
  else:
    return await asyncio.gather(*xs)