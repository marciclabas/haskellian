from typing import Iterable, TypeVar
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
  
  yield from reservoir