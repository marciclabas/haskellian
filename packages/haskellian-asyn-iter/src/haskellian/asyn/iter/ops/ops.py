from typing import AsyncIterable, Awaitable, Callable, TypeVar, Iterable, TypeVarTuple
import os

A = TypeVar("A")
B = TypeVar("B")
As = TypeVarTuple("As")

async def map(f: Callable[[A], B], xs: AsyncIterable[A]) -> AsyncIterable[B]:
  async for x in xs:
    yield f(x)

async def amap(f: Callable[[A], Awaitable[B]], xs: AsyncIterable[A]) -> AsyncIterable[B]:
  async for x in xs:
    yield await f(x)

async def starmap(f: Callable[[*As], B], xs: AsyncIterable[As]) -> AsyncIterable[B]:
  async for x in xs:
    yield f(*x)

async def flatmap(f: Callable[[A], AsyncIterable[B]], xs: AsyncIterable[A]) -> AsyncIterable[B]:
  async for x in xs:
    async for y in f(x):
      yield y

async def filter(p: Callable[[A], bool], xs: AsyncIterable[A]) -> AsyncIterable[A]:
  async for x in xs:
    if p(x):
      yield x

async def concurrent_map(
  f: Callable[[A], Awaitable[B]],
  xs: AsyncIterable[A],
  num_parallel: int | None = None,
) -> AsyncIterable[B]:
  num_parallel = num_parallel or os.cpu_count() or 1
  coros: list[Awaitable[B]] = []
  async for x in xs:
    if len(coros) >= num_parallel:
      yield await coros.pop(0)
    coros.append(f(x))
  for coro in coros:
    yield await coro

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
  return [x async for x in xs]

async def skip(n: int, xs: AsyncIterable[A]) -> AsyncIterable[A]:
  async for i, x in enumerate(xs):
    if i >= n:
      yield x

async def take(n: int, xs: AsyncIterable[A]) -> AsyncIterable[A]:
  if n == 0:
    return
  async for i, x in enumerate(xs):
    if i < n - 1:
      yield x
    elif i >= n - 1:
      yield x
      return

async def split(n: int, xs: AsyncIterable[A]) -> tuple[list[A], AsyncIterable[A]]:
  head = await syncify(take(n, xs))
  return head, xs

async def batch(
  batch_size: int, xs: AsyncIterable[A], yield_remaining: bool = True
) -> AsyncIterable[tuple[A, ...]]:
  batch = []
  async for x in xs:
    if len(batch) == batch_size:
      yield tuple(batch)
      batch = []
    batch.append(x)
  if yield_remaining and len(batch) > 0:
    yield tuple(batch)
