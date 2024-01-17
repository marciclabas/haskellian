"""
- All functions are curried
- Iterable-manipulation functions always return `Generator`
"""
from .fp import vpipe, either, uneither, safe, listify
from .iterables import *
from . import asynch