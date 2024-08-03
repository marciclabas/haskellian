from typing import TypeVar, Mapping, Callable, TypeGuard, overload
import inspect
from haskellian import dicts as D

K = TypeVar('K')
V = TypeVar('V')
K2 = TypeVar('K2')
V2 = TypeVar('V2')
T = TypeVar('T')


@D.lift
def map(f: Callable[[K, V], V2], xs: Mapping[K, V]) -> dict[K, V2]:
  return { k: f(k, v) for k, v in xs.items() }

@D.lift
def map_v(f: Callable[[V], V2], xs: Mapping[K, V]) -> dict[K, V2]:
  return { k: f(v) for k, v in xs.items() }

@D.lift
def map_k(f: Callable[[K], K2], xs: Mapping[K, V]) -> dict[K2, V]:
  return { f(k): v for k, v in xs.items() }

@D.lift
def flatmap(f: Callable[[K, V], Mapping[K2, V2]], xs: Mapping[K, V]) -> dict[K2, V2]:
  out: dict[K2, V2] = {}
  for entry in xs.items():
    out |= f(*entry)
  return out

@D.lift
def flatmap_v(f: Callable[[V], Mapping[K2, V2]], xs: Mapping[K, V]) -> dict[K2, V2]:
  out: dict[K2, V2] = {}
  for _, v in xs.items():
    out |= f(v)
  return out

@D.lift
def flatmap_k(f: Callable[[K], Mapping[K2, V]], xs: Mapping[K, V]) -> dict[K2, V]:
  out: dict[K2, V] = {}
  for k in xs:
    out |= f(k)
  return out

@D.lift
def filter(f: Callable[[K, V], bool], xs: Mapping[K, V]) -> dict[K, V]:
  return { k: v for k, v in xs.items() if f(k, v) }

@D.lift
def filter_v(f: Callable[[V], bool], xs: Mapping[K, V]) -> dict[K, V]:
  return { k: v for k, v in xs.items() if f(v) }

@D.lift
def filter_k(f: Callable[[K], bool], xs: Mapping[K, V]) -> dict[K, V]:
  return { k: v for k, v in xs.items() if f(k) }