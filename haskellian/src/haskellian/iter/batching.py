from typing_extensions import Iterable, TypeVar, Callable
import itertools
from haskellian import iter as I
from .slicing import take

A = TypeVar('A')

def split(n: int, xs: Iterable[A]) -> tuple[list[A], Iterable[A]]:
  """Splits `xs` into a list of the first `n` and a generator of the rest
  - e.g: `split(3, [1,2,3,4,5]) == ([1, 2, 3], generator(4, 5))`"""
  it = iter(xs)
  init = list(take(n, it))
  return init, (x for x in it)

@I.lift
def batch(n: int, xs: Iterable[A]) -> Iterable[tuple[A, ...]]:
  """Batches `xs` into `n`-tuples"""
  it = iter(xs)
  while b := tuple(itertools.islice(it, n)):
    yield b


@I.lift
def shard(xs: Iterable[A], min_size: float, size: Callable[[A], float]) -> Iterable[list[A]]:
  """Shards `xs` into groups of at least `min_size` based on `size` (last shard may have less)"""
  shard = []
  acc = 0
  for x in xs:
    acc += size(x)
    shard.append(x)
    if acc >= min_size:
      yield shard
      shard = []
      acc = 0
  if shard:
    yield shard