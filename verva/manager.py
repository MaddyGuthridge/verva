"""
verva > manager
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .context import VervaContext

class VervaManager:
    """Manages the collection of VervaContext objects, so that they can be
    queried as required
    """

    __contexts: dict[str, VervaContext] = {}

    @classmethod
    def registerContext(cls, c: VervaContext, modules: list[str]) -> None:
        """Register a context with Verva. This should be automatically called
        during context construction
        """
        for m in modules:
            cls.__contexts[m] = c

    @classmethod
    def isRegistered(cls, name: str) -> bool:
        """Returns whether a module is registered with verva

        Args:
            name (str): name of module

        Returns:
            bool: whether it's registered
        """
        return name in cls.__contexts.keys()

    @classmethod
    def clear(cls) -> None:
        """Clear all registered contexts
        """
        cls.__contexts = {}
