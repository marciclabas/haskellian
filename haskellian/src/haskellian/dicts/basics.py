from typing import TypeVar, Mapping, Callable, TypeGuard, overload
import inspect
from haskellian import dicts as D

K = TypeVar('K')
V = TypeVar('V')
K2 = TypeVar('K2')
V2 = TypeVar('V2')
T = TypeVar('T')

Mapper = Callable[[V], T] | Callable[[K, V], T]

def apply(f: Mapper[K, V, T], entry: tuple[K, V]) -> T:
  sig = inspect.signature(f)
  return f(entry[1]) if len(sig.parameters) == 1 else f(*entry) # type: ignore

@D.lift
def map(f: Mapper[K, V, V2], xs: Mapping[K, V]) -> dict[K, V2]:
  return { k: apply(f, (k, v)) for k, v in xs.items() }

@D.lift
def map_k(f: Callable[[K], K2], xs: Mapping[K, V]) -> dict[K2, V]:
  return { apply(f, (k, v)): v for k, v in xs.items() }

@D.lift
def map_kv(f: Mapper[K, V, tuple[K2, V2]], xs: Mapping[K, V]) -> dict[K2, V2]:
  return dict(apply(f, entry) for entry in xs.items())

@D.lift
def flatmap(f: Mapper[K, V, Mapping[K2, V2]], xs: Mapping[K, V]) -> dict[K2, V2]:
  out: dict[K2, V2] = {}
  for entry in xs.items():
    out |= apply(f, entry)
  return out

@D.lift
def flatmap_k(f: Callable[[K], Mapping[K2, V]], xs: Mapping[K, V]) -> dict[K2, V]:
  out: dict[K2, V] = {}
  for k in xs:
    out |= f(k)
  return out

@overload
def filter(f: Mapper[K, V, TypeGuard[tuple[K2, V2]]], xs: Mapping[K, V]) -> 'D.Dict[K2, V2]':
  ...
@overload
def filter(f: Mapper[K, V, TypeGuard[V2]], xs: Mapping[K, V]) -> 'D.Dict[K, V2]':
  ...
@overload
def filter(f: Mapper[K, V, bool], xs: Mapping[K, V]) -> 'D.Dict[K, V]':
  ...
@D.lift
def filter(f: Mapper[K, V, bool], xs: Mapping[K, V]) -> dict[K, V]:
  return { k: v for k, v in xs.items() if apply(f, (k, v)) }

@overload
def filter_k(f: Callable[[K], TypeGuard[K2]], xs: Mapping[K, V]) -> 'D.Dict[K2, V]':
  ...
@overload
def filter_k(f: Callable[[K], bool], xs: Mapping[K, V]) -> 'D.Dict[K, V]':
  ...
@D.lift
def filter_k(f: Callable[[K], bool], xs: Mapping[K, V]) -> dict[K, V]:
  return { k: v for k, v in xs.items() if f(k) }