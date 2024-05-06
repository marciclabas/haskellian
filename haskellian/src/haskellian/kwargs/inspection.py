from inspect import Signature, Parameter

def add_kw(sig: Signature, name: str, type: type) -> Signature:
  """Adds a keyword-only parameter to a signature."""
  params = list(sig.parameters.values())
  params.append(Parameter(name, Parameter.KEYWORD_ONLY, default=None, annotation=type))
  return sig.replace(parameters=params)