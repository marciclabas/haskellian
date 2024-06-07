from typing import Mapping, TypeVar, Callable, Iterable, Sequence
from haskellian import iter as I

A = TypeVar('A')
K = TypeVar('K')
K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')
V1 = TypeVar('V1')
V2 = TypeVar('V2')

def map_v(f: Callable[[V1], V2], d: Mapping[K, V1]) -> dict[K, V2]:
  return { k: f(v) for k, v in d.items() }

def map_k(f: Callable[[K1], K2], d: Mapping[K1, V]) -> dict[K2, V]:
  return { f(k): v for k, v in d.items() }

def map_kv(f: Callable[[K1, V1], tuple[K2, V2]], d: Mapping[K1, V1]) -> dict[K2, V2]:
  return dict(f(k, v) for k, v in d.items())

@I.lift
def zip(xs: Mapping[K, Iterable[V]]) -> Iterable[dict[K, V]]:
  """`zip({ 'a': [1, 2, 3], 'b': [4, 5, 6] }) == [{'a': 1, 'b': 4}, {'a': 2, 'b': 5}, {'a': 3, 'b': 6}]`"""
  iters = {
    key: iter(it)
    for key, it in xs.items()
  }
  while True:
    try:
      yield {
        key: next(it)
        for key, it in iters.items()
      }
    except StopIteration:
      break

def aggregate(f: Callable[[Sequence[V]], A], xs: Sequence[Mapping[K, V]]) -> dict[K, A]:
  """Aggregate values with a same key
  ```
  aggregate(sum, [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}])
  # {'a': 4, 'b': 6}
  ```
  """
  return {
    key: f(list(I.pluck(xs, key)))
    for key in xs[0].keys()
  }