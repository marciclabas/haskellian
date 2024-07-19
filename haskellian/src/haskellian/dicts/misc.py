from typing import Mapping, TypeVar, Callable
from haskellian import dicts as D

K = TypeVar('K')
V = TypeVar('V')
V2 = TypeVar('V2')

def unpack(d: Mapping[K, V], *keys: K) -> tuple[V, ...]:
  return tuple(d[key] for key in keys)


@D.lift
def evolve(mappers: Mapping[K, Callable[[V], V2]], xs: Mapping[K, V]) -> Mapping[K, V|V2]:
  """Applies each mapper to the corresponding key"""
  return { k: mappers.get(k, lambda x: x)(v) for k, v in xs.items() }