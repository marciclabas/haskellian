# `asyn_iter`

The `asyn_iter` module provides both functions and an `AsyncIter` class, a thin wrapper around async generators that allows for lazy evaluation and chaining of operations.

## `AsyncIter[T]`

The most common way to create `AsyncIter`s is to "lift" generator functions:

```python
from haskellian import asyn_iter as AI

@AI.lift
async def gen():
  for i in range(100000000):
    yield i

gen() # AsyncIter[int]
```

### Method Chaining

Many common methods are available for chaining operations. For example:

```python
from haskellian import AsyncIter

await (AsyncIter(range(100000000))
  .filter(lambda x: x % 2 == 0)
  .map(lambda x: x * 2)
  .skip(10)
  .enumerate()
  .every(4)
  .take(5)
  .sync())
# [(0, 40), (4, 56), (8, 72), (12, 88), (16, 104)]
```

## `ManagedAsync[T]`

A `ManagedAsync` lets you programmatically control an `AsyncIterable`. For example:

```python
import asyncio
from haskellian import ManagedAsync

xs = ManagedAsync()

async def pusher():
  for i in range(10):
    await asyncio.sleep(1)
    await xs.push(i)
  await xs.end()

asyncio.create_task(pusher())

async for x in xs:
  print(x) # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
# [end]
```

## Functions

See the [reference](reference/asyn-iter.md) for a full list.


Next up, [`dicts`](dicts.md)