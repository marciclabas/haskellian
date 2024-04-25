from typing_extensions import TypeVar, Mapping, overload

D1 = TypeVar('D1', bound=Mapping)
D2 = TypeVar('D2', bound=Mapping)
D3 = TypeVar('D3', bound=Mapping)

@overload
def split(Params1: type[D1], Params2: type[D2], params: D1 | D2) -> tuple[D1, D2]: ...
@overload
def split(Params1: type[D1], Params2: type[D2], Params3: type[D3], params: D1 | D2 | D3) -> tuple[D1, D2, D3]: ...
def split(Params1: type[D1], Params2: type[D2], x3, x4 = None) -> tuple[Mapping, ...]:
  Params = [Params1, Params2] + (x4 and [x3] or [])
  params = x4 or x3
  return tuple({ k: params[k] for k in getattr(P, '__annotations__', {}) if k in params } for P in Params)