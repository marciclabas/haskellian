from haskellian import DEBUG_IMPORTS, iter as I, promise as P, Promise
if DEBUG_IMPORTS:
  print('Import:', __name__)
from typing_extensions import TypeVar, Callable, Awaitable, Mapping, Iterable, overload
from inspect import isawaitable
import asyncio

A = TypeVar('A')
B = TypeVar('B')

async def then(f: Callable[[A], B], x: Awaitable[A]) -> B:
  return f(await x)

async def bind(f: Callable[[A], Awaitable[B]], x: Awaitable[A]) -> B:
  return await f(await x)

@P.lift
async def of(x: A) -> A:
  return x

@P.lift
async def delay(secs: float):
  await asyncio.sleep(secs)

@P.lift
async def wait(x: A | Awaitable[A]) -> A:
  return await x if isawaitable(x) else x # type: ignore

@overload
def all(xs: Iterable[Awaitable[A]]) -> Promise[list[A]]: ...
@overload
def all(xs: Mapping[str, Awaitable[A]]) -> Promise[dict[str, A]]: ...

@P.lift
async def all(xs):
  if isinstance(xs, Mapping):
    keys, values = I.unzip(xs.items())
    results = await asyncio.gather(*values)
    return dict(zip(keys, results))
  else:
    return await asyncio.gather(*xs)

@P.lift
async def all2d(xxs: Iterable[Iterable[Awaitable[A]]]) -> list[list[A]]:
  return await all([all(xs) for xs in xxs])