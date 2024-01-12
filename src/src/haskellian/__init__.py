"""
- All functions are curried
- Iterable-manipulation functions always return `Generator`
"""
from .fp import vpipe, either, uneither, safe, listify
from .iterables import map, filter, batch, flatmap, flatten, fst, snd, head, tail, take, \
    split, min, sorted, skip, pairwise, transpose, starmap, uncons, unzip, unzipg, pick
from . import asynch