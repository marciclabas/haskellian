from typing import Iterable, Callable, Sequence, TypeVar
import random
from haskellian import iter as I

A = TypeVar('A')

@I.lift
def shuffle(xs: Iterable[A], shuffle_size: int) -> Iterable[A]:
  """Reservoir sampling based shuffling"""
  reservoir = []
  for x in xs:
    if len(reservoir) < shuffle_size:
      reservoir.append(x)
    else:
      i = random.randrange(0, shuffle_size)
      yield reservoir[i]
      reservoir[i] = x
  
  random.shuffle(reservoir)
  yield from reservoir

@I.lift
def repeat(iter: Callable[[], Iterable[A]]) -> Iterable[A]:
  """Repeat a lazy iterable indefinitely"""
  while True:
    yield from iter()

@I.lift
def oversample(data: Sequence[Callable[[], Iterable[A]]]) -> Iterable[A]:
  """Balance lazy iterators by repeating the shorter ones"""
  iters = [iter(repeat(d)) for d in data]
  while True:
    for i in iters:
      yield next(i)

@I.lift
def undersample(data: Sequence[Callable[[], Iterable[A]]]) -> Iterable[A]:
  """Balance lazy iterators by truncating the longer ones"""
  while True:
    for t in zip(*[d() for d in data]):
      yield from t