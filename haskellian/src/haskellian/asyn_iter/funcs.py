from typing_extensions import AsyncIterable, Awaitable, Callable, TypeVar, Iterable, TypeVarTuple, Unpack
from haskellian import asyn_iter as AI

A = TypeVar("A")
B = TypeVar("B")
As = TypeVarTuple("As")

@AI.lift
async def map(f: Callable[[A], B], xs: AsyncIterable[A]) -> AsyncIterable[B]:
  """"""
  async for x in xs:
    yield f(x)

@AI.lift
async def amap(f: Callable[[A], Awaitable[B]], xs: AsyncIterable[A]) -> AsyncIterable[B]:
  """`map` but `f` is async"""
  async for x in xs:
    yield await f(x)

@AI.lift
async def starmap(f: Callable[[Unpack[As]], B], xs: AsyncIterable[tuple[Unpack[As]]]) -> AsyncIterable[B]:
  """"""
  async for x in xs:
    yield f(*x)

@AI.lift
async def flatmap(f: Callable[[A], AsyncIterable[B]], xs: AsyncIterable[A]) -> AsyncIterable[B]:
  """"""
  async for x in xs:
    async for y in f(x):
      yield y

@AI.lift
async def filter(p: Callable[[A], bool], xs: AsyncIterable[A]) -> AsyncIterable[A]:
  """"""
  async for x in xs:
    if p(x):
      yield x

@AI.lift
async def flatten(xxs: AsyncIterable[Iterable[A]]) -> AsyncIterable[A]:
  """Single-level flatten"""
  async for xs in xxs:
    for x in xs:
      yield x

@AI.lift
async def enumerate(xs: AsyncIterable[A]) -> AsyncIterable[tuple[int, A]]:
  """"""
  i = 0
  async for x in xs:
    yield i, x
    i += 1

@AI.lift
async def asyncify(xs: Iterable[A]) -> AsyncIterable[A]:
  """Asyncify an iterable"""
  for x in xs:
    yield x

async def syncify(xs: AsyncIterable[A]) -> list[A]:
  """Await all `xs`"""
  return [x async for x in xs]

async def head(xs: AsyncIterable[A]) -> A | None:
  """Get the first element of `xs`"""
  async for x in xs:
    return x
  
@AI.lift
async def every(n: int, xs: AsyncIterable[A]) -> AsyncIterable[A]:
	"""Take every `n`th element of `xs`
	- `every(3, arange(10)) == AsyncIter([0, 3, 6, 9])`
	"""
	async for i, x in enumerate(xs):
		if i % n == 0:
			yield x

@AI.lift
async def skip(n: int, xs: AsyncIterable[A]) -> AsyncIterable[A]:
  """Skip the first `n` elements of `xs`"""
  async for i, x in enumerate(xs):
    if i >= n:
      yield x

@AI.lift
async def take(n: int, xs: AsyncIterable[A]) -> AsyncIterable[A]:
  """Take the first `n` elements of `xs`"""
  if n == 0:
    return
  async for i, x in enumerate(xs):
    if i < n - 1:
      yield x
    elif i >= n - 1:
      yield x
      return

async def split(n: int, xs: AsyncIterable[A]) -> tuple[list[A], AsyncIterable[A]]:
  """Split `xs` into `xs[:n], xs[n:]`"""
  head = await syncify(take(n, xs))
  return head, xs

@AI.lift
async def batch(
  batch_size: int, xs: AsyncIterable[A], yield_remaining: bool = True
) -> AsyncIterable[tuple[A, ...]]:
  """Batch elements of `xs` into tuples of size `batch_size`"""
  batch = []
  async for x in xs:
    if len(batch) == batch_size:
      yield tuple(batch)
      batch = []
    batch.append(x)
  if yield_remaining and len(batch) > 0:
    yield tuple(batch)
