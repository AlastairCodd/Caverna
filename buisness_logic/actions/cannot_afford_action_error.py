from typing import Any, Dict

from core.enums.caverna_enums import ResourceTypeEnum

class CannotAffordActionError(object):
    def __init__(
            self,
            who: Any,
            what: Any,
            cost: Dict[ResourceTypeEnum, int],
            has: Dict[ResourceTypeEnum, int]) -> None:
        self._who = who
        self._what = what
        self._cost = cost
        self._has = has

    def __str__(self) -> str:
        return self.__format__("1")

    def __format__(self, format_spec: str) -> str:
        newline_separator = ""

        try:
            num_spaces = int(format_spec)
            if num_spaces != 0:
                newline_separator = "\r\n" + " " * num_spaces
        except ValueError:
            pass

        result = f"{self._who} cannot afford {self._what}{newline_separator}(cost: "
        result += ", ".join(f"{cost} {resource.name}" for (resource, cost) in self._cost.items())
        result += f",{newline_separator}{self._who} has: "
        result += ", ".join(f"{cost} {resource.name}" for (resource, cost) in self._has.items())
        result += ")"
        return result

    # don't include player resources here, because they might change depending on ordering, and that wouldn't result in a different error
    def __hash__(self):
        return hash((self._who, self._what, *(tuple(self._cost))))

    def __eq__(self, other) -> bool:
        if not isinstance(other, CannotAffordActionError):
            return false
        result = self._who == other._who and \
                 self._what == other._what and \
                 self._cost == other._cost

        return result
