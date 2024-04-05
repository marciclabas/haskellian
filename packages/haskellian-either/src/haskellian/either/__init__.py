"""
### Haskellian Either
> Simple Either type

- Details
"""
from .type import Either, Left, Right, IsLeft
from .narrowing import is_left, is_right
from .funcs import safe, sequence, maybe, filter, filter_lefts, take_while
try:
  from .extras import *
except ImportError:
  ...