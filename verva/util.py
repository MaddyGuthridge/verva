
from typing import Any

def getSignature(obj: Any) -> str:
    """Returns a string "signature" of a callable, used with Verva to identify
    callables, so that they can be referred to within the rest of

    _extended_summary_

    Args:
        func (Callable): _description_

    Returns:
        str: _description_
    """
    return obj.__module__ + '.' + obj.__qualname__
