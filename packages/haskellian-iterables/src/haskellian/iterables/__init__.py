"""
### Haskellian Iterables
> FP-style functions for generators

- Details
"""
from .basics import isiterable, range
from .curried import map, filter, max, min, sorted, flatmap, flatten, starmap
from .slicing import fst, snd, head, tail, take, skip, take_while
from .zipping import unzip, unzipg, uncons, pairwise
from .nested import nested_map, ndrange, ndenumerate, ndflat, transpose, transpose_ragged
from .batching import batch, split
from .misc import pick
from .generators import returned