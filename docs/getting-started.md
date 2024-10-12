# Getting Started

Haskellian gives you a number of pure functions and utilities grouped in modules. We recommend these standard aliases:

```python
from haskellian import iter as I, either as E, asyn_iter as AI, promise as P
```

- [`iter as I`](iter.md): utilities around the `Iter` monad (a lazy iterable sequence)
- [`either as E`](either.md): around the `Either` mondad
- [`asyn_iter as AI`](asyn_iter.md): around the `AsynIter` monad (a lazy, asynchronously iterable sequence)
- [`promise as P`](promise.md): around the `Promise` monad (a lazy, asynchronously iterable sequence)


Let's start with [`iter`](iter.md)