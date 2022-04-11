
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union, Literal
from itertools import zip_longest


class Inf:
    """Simple infinity representation"""

    def __eq__(self, other: object) -> bool:
        return False

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return False

    def __gt__(self, other):
        return True

    def __repr__(self) -> str:
        return "inf"


VersionExpanded = tuple[Union[int, Inf], ...]
VersionType = Union[int, VersionExpanded, None]


class VersionSpec:

    def __init__(
        self,
        min_version: VersionType,
        max_version: VersionType
    ) -> None:
        if isinstance(min_version, int):
            min_version = (min_version,)
        elif min_version is None:
            min_version = (0,)
        if isinstance(max_version, int):
            max_version = (max_version,)
        elif max_version is None:
            max_version = (Inf(),)
        self._min = min_version
        self._max = max_version

        # Check that min < max
        if not self.__tuple_lt(self._min, self._max):
            raise ValueError("Minimum version must be < maximum version")

    def __repr__(self) -> str:
        start = ""
        end = ""
        if self._min is None and self._max is None:
            end = "any"
        if self._max is not None:
            end = f"< {'.'.join(map(str, self._max))} "
        if self._min is not None:
            start = f">= {'.'.join(map(str, self._min))}"
        return f"VersionSpec( {start}, {end})"

    @staticmethod
    def __tuple_lt(
        a: VersionExpanded,
        b: VersionExpanded,
        eq: bool = False,
    ) -> bool:
        """Return whether a < b for tuples
        """
        for a_, b_ in zip_longest(a, b, fillvalue=0):
            if a_ < b_:
                return True
            elif a_ > b_:
                return False
        return eq

    def __contains__(self, obj: Any) -> bool:
        """Return whether a version is contained within this version range
        """
        e = "Version numbers should be of type int or tuple[int, ...]"
        if isinstance(obj, int):
            obj = (obj,)
        elif not isinstance(obj, tuple):
            raise TypeError(e)
        for ele in obj:
            if not isinstance(ele, int):
                raise TypeError(e)

        # Check version by version
        return (
            self.__tuple_lt(self._min, obj, eq=True)
            and self.__tuple_lt(obj, self._max)
        )

    def __do_overlap(self, other: VersionSpec) -> bool:
        """Implementation of overlap() function, behaving one way
        """
        return (
            # Our minimum value is less than their minimum
            self.__tuple_lt(self._min, other._min, eq=True)
            # And our maximum value is greater than their minimum
            and self.__tuple_lt(other._min, self._max)
        )

    def overlap(self, other: VersionSpec) -> bool:
        """Returns whether two VersionSpec objects overlap

        Args:
            other (VersionSpec): other version spec

        Returns:
            bool: whether they overlap
        """
        return self.__do_overlap(other) or other.__do_overlap(self)
