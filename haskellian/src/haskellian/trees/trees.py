from typing import TypeVar, Mapping, Sequence, Iterable, Callable
from haskellian import iter as I

A = TypeVar('A')
B = TypeVar('B')
T = TypeVar('T')

Tree = T | Mapping[str, 'Tree[T]']

@I.lift
def flatten(tree: Tree[T], prefix: tuple[str|int, ...] = ()) -> Iterable[tuple[Sequence[str|int], T]]:
  if isinstance(tree, Mapping):
    for k, v in tree.items():
      yield from flatten(v, prefix + (k,))
  elif isinstance(tree, Sequence):
    for i, v in enumerate(tree):
      yield from flatten(v, prefix + (i,))
  else:
    yield prefix, tree


def map(tree: Tree[A], f: Callable[[A], B]) -> Tree[B]:
  if isinstance(tree, Mapping):
    return {k: map(v, f) for k, v in tree.items()}
  else:
    return f(tree)
  
def path_map(tree: Tree[A], f: Callable[[Sequence[str], A], B], prefix: tuple[str, ...] = ()) -> Tree[B]:
  if isinstance(tree, Mapping):
    return {k: path_map(v, f, prefix + (k,)) for k, v in tree.items()}
  else:
    return f(prefix, tree)