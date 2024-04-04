from typing import TypeVar, Callable, Iterable, Union, get_args, get_type_hints
from functools import wraps
from .type import Either, Left, Right

R = TypeVar('R')
L = TypeVar('L')

def safe(func: Callable[[], R]) -> 'Either[Exception, R]':
    try:
      return Right(func())
    except Exception as e:
      return Left(e)
    
def maybe(x: R | None) -> 'Either[None, R]':
  return Left() if x is None else Right(x)
    
def sequence(eithers: Iterable[Either[L, R]]) -> Either[list[L], list[R]]:
  """List of lefts if any (thus with length in `[1, len(eithers)]`), otherwise list of all rights (with length `len(eithers)`)"""
  lefts: list[L] = []
  rights: list[R] = []
  for x in eithers:
    x.match(lefts.append, rights.append)
  return Right(rights) if lefts == [] else Left(lefts)

def secure(*Exceptions: type[BaseException]):
  """Secure a function that throws some of `Exceptions` into one that returns `Either[Exceptions, R]` (doesn't catch other exceptions)"""
  def decorator(func: Callable[..., R]):
    @wraps(func)
    def _f(*args, **kwargs) -> Either[Union[*Exceptions], R]:
      try:
        return Right(func(*args, **kwargs))
      except Exceptions as e:
        return Left(e)
    return _f
  return decorator

def secure_coro(*Exceptions: type[BaseException]):
  """Secure a coroutine that throws some of `Exceptions` into one that returns `Either[Exceptions, R]` (doesn't catch other exceptions)"""
  def decorator(func: Callable[..., R]):
    @wraps(func)
    async def _f(*args, **kwargs) -> Either[Union[*Exceptions], R]:
      try:
        return Right(await func(*args, **kwargs))
      except Exceptions as e:
        return Left(e)
    return _f
  return decorator

def secured_exceptions(secured_fn) -> list[type[BaseException]]:
  """Exceptions returned by a function decorated with `secure`"""
  ret = get_type_hints(secured_fn)['return']
  return get_args(get_args(ret)[0])