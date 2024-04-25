from typing_extensions import TypeVar
from .either import Either
from .funcs import safe
from pydantic import BaseModel, ValidationError

T = TypeVar('T', bound=BaseModel)

def validate(data, Model: type[T]) -> Either[ValidationError, T]:
  return safe(lambda: Model.model_validate(data), ValidationError)

def validate_json(data: str | bytes | bytearray, Model: type[T]) -> Either[ValidationError, T]:
  return safe(lambda: Model.model_validate_json(data), ValidationError)
