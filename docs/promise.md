# `promise`

## `ManagedPromise[T]`

The `ManagedPromise` allows you to programmatically control a `Promise`. For example:

```python
import asyncio
from haskellian import ManagedPromise

promise = ManagedPromise[int]()

async def resolver():
  await asyncio.sleep(5)
  promise.resolve(42)

asyncio.create_task(resolver())

print(await promise) # 42 (after 5 seconds)
```
