from typing import Iterable

def isiterable(x, str_iterable = False, bytes_iterable = False) -> bool:
    """Is `x` iterable?
    - `str_iterable`, `bytes_iterable`: wheter `str` and `bytes` are considered iterable
    """
    return isinstance(x, Iterable) and \
      (not isinstance(x, str) or str_iterable) and \
      (not isinstance(x, bytes) or bytes_iterable)

def range(start: int = 0, end: int = None, step: int = None) -> Iterable[int]:
  """Possibly infinite range"""
  i = start
  while end is None or i < end:
    yield i
    i += step