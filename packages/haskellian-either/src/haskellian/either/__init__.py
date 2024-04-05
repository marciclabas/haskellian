"""
### Haskellian Either
> Simple Either type

- Details
"""
from .type import Either, Left, Right, IsLeft
from .funcs import safe, sequence, maybe, filter, filter_lefts
try:
  from .extras import *
except ImportError:
  ...