from typing import Generic, TypeVar, Literal
from dataclasses import dataclass

L = TypeVar('L')
R = TypeVar('R')

@dataclass
class Either(Generic[L, R]):
  value: L | R
  tag: Literal['left', 'right']

@dataclass
class Left(Either[L, R], Generic[L, R]):
  value: L
  tag: Literal['left'] = 'left'

@dataclass
class Right(Either[L, R], Generic[L, R]):
  value: R
  tag: Literal['right'] = 'right'