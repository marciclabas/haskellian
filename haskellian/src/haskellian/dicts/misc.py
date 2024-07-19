from typing import Mapping, TypeVar, Callable, overload
from haskellian import dicts as D
from ramda import curry

K = TypeVar('K')
V = TypeVar('V')
V2 = TypeVar('V2')

def unpack(d: Mapping[K, V], *keys: K) -> tuple[V, ...]:
  return tuple(d[key] for key in keys)


@overload
def evolve(mappers: Mapping[K, Callable[[V], V2]], xs: Mapping[K, V]) -> 'D.Dict[K, V|V2]': ...
@overload
def evolve(mappers: Mapping[K, Callable[[V], V2]]) -> Callable[[Mapping[K, V]], 'D.Dict[K, V|V2]']: ...
@curry
def evolve(mappers, xs): # type: ignore
  """Applies each mapper to the corresponding key"""
  return D.Dict({ k: mappers.get(k, lambda x: x)(v) for k, v in xs.items() })