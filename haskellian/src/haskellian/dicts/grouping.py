from typing import Mapping, TypeVar, Callable, Iterable, Sequence, TypeGuard, overload
from haskellian import iter as I, dicts as D

A = TypeVar('A')
K = TypeVar('K')
K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')
V1 = TypeVar('V1')
V2 = TypeVar('V2')

@D.lift
def group_by(f: Callable[[V], K], xs: Iterable[V]) -> dict[K, list[V]]:
  """Group elements by a function"""
  from collections import defaultdict
  d = defaultdict(list)
  for x in xs:
    d[f(x)].append(x)
  return dict(d)

@I.lift
def zip(xs: Mapping[K, Iterable[V]]) -> Iterable['D.Dict[K, V]']:
  """`zip({ 'a': [1, 2, 3], 'b': [4, 5, 6] }) == [{'a': 1, 'b': 4}, {'a': 2, 'b': 5}, {'a': 3, 'b': 6}]`
  - Ignores keys with non-iterable values
  """
  iters = {
    key: iter(it)
    for key, it in xs.items()
      if I.isiterable(it)
  }
  while True:
    try:
      yield D.Dict({
        key: next(it)
        for key, it in iters.items()
      }) # type: ignore
    except StopIteration:
      break

@D.lift
def unzip(xs: Sequence[Mapping[K, V]]) -> dict[K, list[V]]:
  """`unzip([{'a': 1, 'b': 4}, {'a': 2, 'b': 5}, {'a': 3, 'b': 6}]) == { 'a': [1, 2, 3], 'b': [4, 5, 6] }`"""
  from collections import defaultdict
  out = defaultdict(list)
  for x in xs:
    for key, value in x.items():
      out[key].append(value)
  return dict(out)

@D.lift
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

