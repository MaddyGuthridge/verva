
from typing import Callable

def getCallableSignature(func: Callable) -> str:
    """Returns a string "signature" of a callable, used with Verva to identify
    callables, so that they can be referred to within the rest of

    _extended_summary_

    Args:
        func (Callable): _description_

    Returns:
        str: _description_
    """
    return func.__module__ + '.' + func.__qualname__
