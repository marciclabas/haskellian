from typing import TypeVar, Generic, Callable

A = TypeVar('A')
class Thunk(Generic[A]):
    """A lazy initialized value"""
    _supplier: Callable[[], A]
    _value: A | None = None
    
    def __init__(self, supplier: Callable[[], A]):
        self._supplier = supplier
        
    def __call__(self) -> A:
        if self._value is None:
            self._value = self._supplier()
        return self._value