from math import floor
from typing import Dict, List

from core.baseClasses.base_effect import BaseEffect
from core.enums.caverna_enums import ResourceTypeEnum


class ReceiveWhenReceivingEffect(BaseEffect):
    def __init__(
            self,
            receive: Dict[ResourceTypeEnum, int],
            when_receiving: Dict[ResourceTypeEnum, int]) -> None:
        if receive is None:
            raise ValueError("Receive cannot be null")
        if when_receiving is None:
            raise ValueError("when_receiving cannot be null")

        self._receive: Dict[ResourceTypeEnum, int] = receive
        self._proportional_to: Dict[ResourceTypeEnum, int] = when_receiving
        BaseEffect.__init__(self)

    def invoke(
            self,
            receiving: Dict[ResourceTypeEnum, int]) -> Dict[ResourceTypeEnum, int]:
        if receiving is None:
            raise ValueError("Receviing may not be null")

        number_of_resources_proportional_to: List[int] = [floor(receiving.get(r, 0) / self._proportional_to[r]) for r in self._proportional_to]

        amount_to_receive_multiplier: int = min(number_of_resources_proportional_to)

        resources_to_give: Dict[ResourceTypeEnum, int] = {r: amount_to_receive_multiplier * self._receive[r] for r in self._receive}
        return resources_to_give
