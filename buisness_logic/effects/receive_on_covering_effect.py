from math import floor
from typing import Dict, List

from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ResourceTypeEnum


class ReceiveOnCoveringEffect(BaseEffect):
    def __init__(
            self,
            items_to_receive: Dict[ResourceTypeEnum, int]):
        if items_to_receive is None:
            raise ValueError("Items to receive cannot be null")

        self._items_to_receive: Dict[ResourceTypeEnum, int] = items_to_receive

    @property
    def resources(self) -> Dict[ResourceTypeEnum, int]:
        return self._items_to_receive

    def __format__(self, format_spec):
        text = [("", "receive ")]

        for (i, (resource, amount)) in enumerate(self._items_to_receive.items()):
           text.append(("class:count", str(amount)))
           text.append(("", " "))
           text.append(("", resource.name))
           if i != len(self._items_to_receive) - 1:
               text.append(("", ", "))

        if format_spec == "pp":
            return text
        if format_spec.isspace():
            return "".join(e[1] for e in text)
        raise ValueError("format parameter must be 'pp' or whitespace/empty")
