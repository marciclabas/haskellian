"""
- All functions are curried
- Iterable-manipulation functions always return `Generator`
"""
from .main import vpipe, either, uneither, safe, listify
from .thunk import Thunk
from .iterables import *
from . import asynch