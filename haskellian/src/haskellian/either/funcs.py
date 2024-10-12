from typing_extensions import TypeVar, Callable, Iterable, ParamSpec, Generic, overload, \
  Awaitable, Coroutine, get_args
from inspect import iscoroutinefunction
from functools import wraps
from .either import Either, Left, Right

A = TypeVar('A')
R = TypeVar('R')
L = TypeVar('L')
P = ParamSpec('P')
Err = TypeVar('Err')


class safe(Generic[Err]):
  """A decorator to catch exceptions and return them as `Left`.
  
  ```python
  @E.safe[OSError]()
  def safe_write(path: str, content: bytes):
    with open(path, 'wb') as f:
      f.write(content)

  result = safe_write('file.txt', b'content') # Either[OSError, None]
  ```
  """

  @property
  def exc(self) -> type[Err]:
    return get_args(self.__orig_class__)[0] # type: ignore (yep, typing internals are messed up)

  @overload
  def __call__(self, fn: Callable[P, Coroutine[None, None, R]]) -> Callable[P, Coroutine[None, None, Either[Err, R]]]: # type: ignore
    ...
  @overload
  def __call__(self, fn: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[Either[Err, R]]]: # type: ignore
    ...
  @overload
  def __call__(self, fn: Callable[P, R]) -> Callable[P, Either[Err, R]]:
    ...
  
  def __call__(self, fn): # type: ignore
    if iscoroutinefunction(fn):
      @wraps(fn)
      async def _wrapper(*args: P.args, **kwargs: P.kwargs):
        try:
          return Right(await fn(*args, **kwargs))
        except Exception as e:
          if isinstance(e, self.exc):
            return Left(e)
          raise e
      return _wrapper
    else:
      @wraps(fn)
      def wrapper(*args: P.args, **kwargs: P.kwargs):
        try:
          return Right(fn(*args, **kwargs))
        except Exception as e:
          if isinstance(e, self.exc):
            return Left(e)
          raise e
      return wrapper
    

def maybe(x: R | None) -> 'Either[None, R]':
  """Converts a nullable value to `Either`"""
  return Left(None) if x is None else Right(x)

def get_or(default: A) -> Callable[[Either[L, R]], R | A]:
  return lambda e: e.get_or(default)

def unsafe(x: Either[L, R]) -> R:
  return x.unsafe()
    
def sequence(eithers: Iterable[Either[L, R]]) -> Either[list[L], list[R]]:
  """List of lefts if any, otherwise list of all rights.
  
  ```python
  E.sequence([Left(1), Right(2), Right(3), Left(4)]) # Left([1, 4])
  E.sequence([Right(2), Right(3)]) # Right([2, 3])
  ```
  """
  lefts: list[L] = []
  rights: list[R] = []
  for x in eithers:
    x.match(lefts.append, rights.append)
  return Right(rights) if lefts == [] else Left(lefts)

def filter(eithers: Iterable[Either[L, R]]) -> Iterable[R]:
  """"""
  for e in eithers:
    match e:
      case Right(value):
        yield value

def filter_lefts(eithers: Iterable[Either[L, R]]) -> Iterable[L]:
  """"""
  for e in eithers:
    match e:
      case Left(err):
        yield err

def take_while(eithers: Iterable[Either[L, R]]) -> Iterable[R]:
  """"""
  for e in eithers:
    match e:
      case Right(x):
        yield x
      case _:
        return