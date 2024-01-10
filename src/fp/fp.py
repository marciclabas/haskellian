from typing import TypeVar, Iterable, Callable
from functools import wraps
import ramda as R

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def vpipe(x: A, *fs: Callable[[A], B]) -> B:
    return R.pipe(*fs)(x)

def safe(f: Callable[[], A], default: A = None) -> A:
    try:
        return f()
    except:
        return default
    
def either(f: Callable[[], A]) -> A | Exception:
    try:
        return f()
    except Exception as e:
        return e
    
def uneither(x: A | Exception) -> A:
    match x:
        case Exception():
            raise x
        case _:
            return x
        
def listify(f: Callable[[A], Iterable[B]]) -> Callable[[A], list[B]]:
    @wraps(f)
    def _f(*args, **kwargs):
        return list(f(*args, **kwargs))
    return _f