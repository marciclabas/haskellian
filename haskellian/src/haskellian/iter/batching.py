from haskellian import DEBUG_IMPORTS, iter as I
if DEBUG_IMPORTS:
  print('Import:', __name__)
from typing_extensions import Iterable, TypeVar
import itertools
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

