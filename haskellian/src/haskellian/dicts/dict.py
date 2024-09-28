from typing_extensions import Callable, Generic, TypeVar, Mapping, Iterable, Any
from haskellian import Monad, dicts as D, iter as I

K = TypeVar('K')
K2 = TypeVar('K2')
V = TypeVar('V')
V2 = TypeVar('V2')

class Dict(Monad[tuple[K, V]], dict[K, V], Generic[K, V]):
  """A monadic, fluent `dict`"""
  
  def __repr__(self):
    return f'Dict({super().__repr__()})'

  @classmethod
  def of(cls, x: tuple[K, V]): # type: ignore
    return cls(dict([x]))
  
  def flatmap(self, f: Callable[[K, V], Mapping[K2, V2]]) -> 'Dict[K2, V2]':
    return D.flatmap(f, self)
  
  bind = flatmap # type: ignore

  def flatmap_k(self, f: Callable[[K], Mapping[K2, V]]) -> 'Dict[K2, V]':
    return D.flatmap_k(f, self)
  
  def flatmap_v(self, f: Callable[[V], Mapping[K, V2]]) -> 'Dict[K, V2]':
    return D.flatmap_v(f, self)
  
  def map(self, f: Callable[[K, V], V2]) -> 'Dict[K, V2]':
    return D.map(f, self)
  
  def map_v(self, f: Callable[[V], V2]) -> 'Dict[K, V2]':
    return D.map_v(f, self)
  
  def map_k(self, f: Callable[[K], K2]) -> 'Dict[K2, V]':
    return D.map_k(f, self)
  
  def filter(self, p):
    return D.filter(p, self)
  
  def filter_k(self, f):
    return D.filter_k(f, self)
  
  def filter_v(self, f):
    return D.filter_v(f, self)
  
  def zip(self, f: Callable[[V], Iterable[V2]] = lambda x: x) -> 'I.Iter[Dict[K, V2]]': # type: ignore
    """By default, `zip({ 'a': [1, 2, 3], 'b': [4, 5, 6] }) == [{'a': 1, 'b': 4}, {'a': 2, 'b': 5}, {'a': 3, 'b': 6}]`
    - Note: perhaps `f` is useful for something else, but it's just a dummy to make the types work.
    """
    return D.zip(self.map(f)) # type: ignore

  def unpack(self, *keys: K) -> tuple[V, ...]:
    return D.unpack(self, *keys)
  
  def evolve(self, mappers: Mapping[K, Callable[[V], V2]]) -> 'Dict[K, V|V2]':
    return D.evolve(mappers, self)
  
  def group_by(self, f: Callable[[K, V], K2]) -> 'Dict[K2, Dict[K, V]]':
    return D.group_by(lambda t: f(*t), self.items()).map_v(Dict)
  
  def sorted(self, key: Callable[[K, V], Any]) -> list[V]:
    return [v for _, v in sorted(self.items(), key=lambda t: key(*t))]