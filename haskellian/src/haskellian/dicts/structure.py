from typing import Mapping, TypeVar

K = TypeVar('K')
V = TypeVar('V')

def unpack(d: Mapping[K, V], *keys: K) -> tuple[V, ...]:
  return tuple(d[key] for key in keys)