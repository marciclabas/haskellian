from typing_extensions import Callable, Generic, TypeVar, Mapping, Iterable, overload, TypeGuard
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
  def of(cls, x: tuple[K, V]):
    return cls(dict([x]))
  
  def flatmap(self, f: 'D.Mapper[K, V, Mapping[K2, V2]]') -> 'Dict[K2, V2]':
    return D.flatmap(f, self)
  
  bind = flatmap # type: ignore

  def flatmap_k(self, f: Callable[[K], Mapping[K2, V]]) -> 'Dict[K2, V]':
    return D.flatmap_k(f, self)
  
  @overload
  def map(self, f: 'D.Mapper[K, V, V]') -> 'Dict[K, V]':
    ...
  @overload
  def map(self, f: 'D.Mapper[K, V, V2]') -> 'Dict[K, V2]':
    ...
  def map(self, f: 'D.Mapper[K, V, V2]') -> 'Dict[K, V2]':
    return D.map(f, self)
  
  @overload
  def map_k(self, f: Callable[[K], K]) -> 'Dict[K, V]':
    ...
  @overload
  def map_k(self, f: Callable[[K], K2]) -> 'Dict[K2, V]':
    ...
  def map_k(self, f: Callable[[K], K2]) -> 'Dict[K2, V]':
    return D.map_k(f, self)
  
  def map_kv(self, f: 'D.Mapper[K, V, tuple[K2, V2]]') -> 'Dict[K2, V2]':
    return D.map_kv(f, self)
  
  @overload
  def filter(self, p: 'D.Mapper[K, V, TypeGuard[V2]]') -> 'Dict[K, V2]':
    ...
  @overload
  def filter(self, p: 'D.Mapper[K, V, bool]') -> 'Dict[K, V]':
    ...
  def filter(self, p):
    return D.filter(p, self)
  
  @overload
  def filter_k(self, f: Callable[[K], TypeGuard[K2]]) -> 'D.Dict[K2, V]':
    ...
  @overload
  def filter_k(self, f: Callable[[K], bool]) -> 'D.Dict[K, V]':
    ...
  def filter_k(self, f):
    return D.filter_k(f, self)
  
  def zip(self, f: Callable[[V], Iterable[V2]] = lambda x: x) -> 'I.Iter[Dict[K, V2]]': # type: ignore
    """By default, `zip({ 'a': [1, 2, 3], 'b': [4, 5, 6] }) == [{'a': 1, 'b': 4}, {'a': 2, 'b': 5}, {'a': 3, 'b': 6}]`
    - Note: perhaps `f` is useful for something else, but it's just a dummy to make the types work.
    """
    return D.zip(self.map(f)) # type: ignore
