"""
### Haskellian Either
> Simple Either type

- Details
"""
from .type import Either, Left, Right
from .funcs import safe, unsafe, bind, fmap, match