"""
context.py

Contains the definition for a Verva Context, which is used to allow a
package to manage its front-facing functions and document their version
requirements.
"""

from typing import TypeVar, Generic, Callable, Union
from verva.util import getSignature
from verva.manager import VervaManager
from verva.version import VersionSpec, VersionType
from verva.exceptions import (
    OverlappingVersionException,
    SignatureNotFoundException,
    NoMatchingVersionException,
)

T = TypeVar('T', bound=Callable)


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

    @property
    def version(self) -> VersionSpec:
        return self._version


class VervaContext:
    """
    VervaContext objects are used by packages to manage all the functions
    provided by the package, allowing Verva to check API version numbers
    against target version numbers.
    """

    def __init__(
        self,
        name: str,
        mapped_imports: list[str],
    ) -> None:
        """Create a VervaContext

        This is used by packages to manage all the functions provided by the
        package, allowing Verva to check API version numbers against target
        version numbers.

        Args:
            name (str): name of the context

            mapped_imports (list[str]): list of module names that this context
            should be mapped to
        """
        self._name = name
        # For now we'll only manage basic functions
        self._originals: dict[str, Callable] = {}
        self._items: dict[str, list[ItemContainer[Callable]]] = {}
        VervaManager.registerContext(self, mapped_imports)

    def register(
        self,
        applies_to: Callable,
        min_version: VersionType = None,
        max_version: VersionType = None,
    ):
        """Decorate a function with Verva, registering its existence

        This function should be used as a decorator.

        Args:
            applies_to (Callable): original function that we are adding an
            alternate interface to

            min_version (VersionSpec): minimum version to call this function

            max_version (VersionSpec): maximum version to call this function

        Raises:
            OverlappingVersionException: this function's versions overlap
                with another already registered version

        Decorates:
            func (Callable): function to register
        """
        def wrapper(obj: Callable) -> Callable:
            # Get the location of the callable, for lookup later
            sign = getSignature(applies_to)
            # Check that the version spec is valid
            v = VersionSpec(min_version, max_version)
            for item in self._items.get(sign, []):
                if v.overlap(item.version):
                    raise OverlappingVersionException(
                        "Can't register overlapping version")
            # Append to the list of implementations of that sign
            self._items[sign] = self._items.get(sign, []) + [
                ItemContainer(obj, v)
            ]
            return obj
        return wrapper

    def is_registered(self, func: Union[str, Callable]) -> bool:
        """Returns whether func is registered with this context

        Args:
            func (str | Callable): either the function to check or the
                signature string of it

        Returns:
            bool: whether obj is registered
        """
        if not isinstance(func, str):
            func = getSignature(func)
        return func in self._items

    def num_versions(self, sign: str) -> int:
        """Return the number of different versions of obj registered with this
        context

        Args:
            sign (str): the signature string to query

        Returns:
            int: the number of times obj is registered
        """
        return len(self._items.get(sign, []))

    def get_version_mapping(
        self,
        signature: str,
        target_version: VersionType
    ) -> Callable:
        """Returns a mapping to a registered value if  a mapping exists for the
        target version

        Args:
            signature (str): signature to search for
            target_version (VersionType): API version to target

        Raises:
            SignatureNotFoundException: no mapping found for signature
            NoMatchingVersionException: no version of the target

        Returns:
            Registerable: value registered to that function
        """
        if signature not in self._items:
            raise SignatureNotFoundException("No mapping found for signature")

        for item in self._items[signature]:
            if target_version in item.version:
                return item.item
        raise NoMatchingVersionException("No matching version found for item")
