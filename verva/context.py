"""
context.py

Contains the definition for a Verva Context, which is used to allow a
package to manage its front-facing functions and document their version
requirements.
"""

from typing import Callable, TypeVar
from typing_extensions import ParamSpec

P = ParamSpec('P')
T = TypeVar('T')

class VervaContext:

    def __init__(self, name: str) -> None:
        """Create a VervaContext

        This is used by packages to manage all the functions provided by the
        package, allowing Verva to check API version numbers against target
        version numbers.

        Args:
            name (str): name of the context
        """
        self._name = name
        # For now we'll only manage basic functions
        self._functions: dict[str, Callable] = {}

    def register(self, func: Callable[P, T]) -> Callable[P, T]:
        """Register a function with Verva

        This function should be used as a decorator.

        Args:
            func (Callable): function to register

        Returns:
            Callable: the same function
        """
        # Get the location of the callable, for lookup later
        return func
