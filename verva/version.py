
from typing import TYPE_CHECKING, Any, Union
from itertools import zip_longest

VersionType = Union[int, tuple[int, ...], None]

class VersionSpec:

    def __init__(
        self,
        min_version: VersionType,
        max_version: VersionType
    ) -> None:
        if isinstance(min_version, int):
            min_version = (min_version,)
        if isinstance(max_version, int):
            max_version = (max_version,)
        self._min = min_version
        self._max = max_version

    def __repr__(self) -> str:
        start = ""
        end = ""
        if self._min is None and self._max is None:
            end = "any"
        if self._max is not None:
            end = f"< {'.'.join(map(str, self._max))} "
        if self._min is not None:
            start = f">= {'.'.join(map(str, self._min))}"
        return f"VersionSpec( {start}{end})"

    def __check_min(self, obj: tuple[int, ...]) -> bool:
        if self._min is None:
            return True
        for min_e, act_e in zip_longest(self._min, obj, fillvalue=0):
            if act_e < min_e:
                return False
        return True
    def __check_max(self, obj: tuple[int, ...]) -> bool:
        if self._max is None:
            return True
        for max_e, act_e in zip_longest(self._max, obj, fillvalue=0):
            if act_e > max_e:
                return False
        return not obj == self._max

    def __contains__(self, obj: Any) -> bool:
        if isinstance(obj, int):
            obj = (obj,)
        elif not isinstance(obj, tuple):
            raise TypeError(
                "Version numbers should be of type int or tuple[int, ...]"
            )
        for ele in obj:
            if not isinstance(ele, int): raise TypeError(
                "Version numbers should be of type int or tuple[int, ...]"
            )

        # Check version by version
        return self.__check_min(obj) and self.__check_max(obj)
