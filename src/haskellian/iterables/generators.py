from typing import Generator, TypeVar, Iterable, Callable

A = TypeVar('A')
B = TypeVar('B')


def returned(xs: Generator[A, None, B]) -> tuple[Iterable[A], Callable[[], B | None]]:
  """Iterates a `Generator` `xs` and exposes its return value when fully consumed
  
  E.g:
  ```
  def mygenerator(n: int):
    for i in range(n):
      yield i
    return 'Done!'
    
  xs, ret = iterate(mygenerator(5))
  for x in xs:
    print(ret()) # None
  ret() # 'Done'
  ```
  """
  obj = {}
  def _iter():
    try:
      while True:
        x = next(xs)
        yield x
    except StopIteration as e:
      obj['value'] = e.value
  return _iter(), lambda: obj.get('value')