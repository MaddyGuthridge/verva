"""
context.py

Contains the definition for a Verva Context, which is used to allow a
package to manage its front-facing functions and document their version
requirements.
"""

from typing import Any, TypeVar, Generic, Union, Optional
from verva.util import getSignature
from verva.version import VersionSpec, VersionType

T = TypeVar('T')

class ItemContainer(Generic[T]):
    """A simple container for items registered with Verva
    """
    def __init__(
        self,
        item: T,
        version: VersionSpec,
    ) -> None:
        self._item = item
        self._version = version

    @property
    def item(self) -> T:
        return self._item

class VervaContext:
    """
    VervaContext objects are used by packages to manage all the functions
    provided by the package, allowing Verva to check API version numbers
    against target version numbers.
    """

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
        self._items: dict[str, list[ItemContainer]] = {}


    def register(
        self,
        min_version: VersionType = None,
        max_version: VersionType = None,
    ):
        """Decorate a function with Verva, registering its existence

        This function should be used as a decorator.

        Args:
            min_version (VersionSpec): minimum version to call this function
            max_version (VersionSpec): maximum version to call this function

        Decorates:
            func (Callable): function to register
        """
        def wrapper(self, obj: T) -> T:
            # Get the location of the callable, for lookup later
            sign = getSignature(obj)
            self._items[sign] = ItemContainer(
                obj,
                VersionSpec(min_version, max_version)
            )
            return obj
        return wrapper
