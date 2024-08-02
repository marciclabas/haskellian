from typing import Mapping, TypeVar, Callable, overload
from haskellian import dicts as D
from ramda import curry

K = TypeVar('K')
V = TypeVar('V')
K2 = TypeVar('K2')
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


@overload
def insert(k: K, v: V, xs: Mapping[K, V]) -> 'D.Dict[K, V]': ...
@overload
def insert(k: K, v: V) -> Callable[[Mapping[K, V]], 'D.Dict[K, V]']: ...
@curry
def insert(k, v, xs): # type: ignore
  return D.Dict({**xs, k: v})

@overload
def remove(k: K, xs: Mapping[K, V]) -> 'D.Dict[K, V]': ...
@overload
def remove(k: K) -> Callable[[Mapping[K, V]], 'D.Dict[K, V]']: ...
@curry
def remove(key, xs): # type: ignore
  return D.Dict({k: v for k, v in xs.items() if k != key})

@overload
def rename(k1: K, k2: K2, xs: Mapping[K, V]) -> 'D.Dict[K|K2, V]': ...
@overload
def rename(k1: K, k2: K2) -> Callable[[Mapping[K, V]], 'D.Dict[K|K2, V]']: ...
@curry
def rename(k1, k2, xs): # type: ignore
  return D.Dict({**remove(k1, xs), k2: xs[k1]} if k1 in xs else xs)