from math import floor
from typing import Dict, List

from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ResourceTypeEnum
from localised_resources.localiser import format_resource_dict


class ReceiveWhenReceivingEffect(BaseEffect):
    def __init__(
            self,
            items_to_receive: Dict[ResourceTypeEnum, int],
            when_receiving_items: Dict[ResourceTypeEnum, int]) -> None:
        if items_to_receive is None:
            raise ValueError("Items to receive cannot be null")
        if when_receiving_items is None:
            raise ValueError("When receiving items cannot be null")

        self._items_to_receive: Dict[ResourceTypeEnum, int] = items_to_receive
        self._when_receiving_items: Dict[ResourceTypeEnum, int] = when_receiving_items

    def invoke(
            self,
            items_received: Dict[ResourceTypeEnum, int]) -> Dict[ResourceTypeEnum, int]:
        if items_received is None:
            raise ValueError("Receiving may not be null")

        number_of_resources_proportional_to: List[int] = [floor(items_received.get(r, 0) / self._when_receiving_items[r]) for r in self._when_receiving_items]

        amount_to_receive_multiplier: int = min(number_of_resources_proportional_to)

        resources_to_give: Dict[ResourceTypeEnum, int] = {r: amount_to_receive_multiplier * self._items_to_receive[r] for r in self._items_to_receive}
        return resources_to_give

    def __str__(self) -> str:
        receive_readable: str = format_resource_dict(self._items_to_receive, " and ")
        when_receiving_readable: str = format_resource_dict(self._when_receiving_items, " and ")
        result: str = f"Receive {receive_readable} when receiving {when_receiving_readable}"
        return result
