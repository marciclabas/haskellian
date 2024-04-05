try:
  from .pydantic import validate, validate_json
except ImportError:
  ...