from typing import Dict

from common.entities.dwarf import Dwarf
from common.entities.player import Player
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum
from core.baseClasses.base_action import BaseAction


class PayAction(BaseAction):
    def __init__(self, pay_items: Dict[ResourceTypeEnum, int]):
        if pay_items is None:
            raise ValueError("payItems")
        self._payItems: Dict[ResourceTypeEnum, int] = pay_items

    def invoke(self, player: Player, active_card: ResourceContainer, current_dwarf: Dwarf) -> bool:
        if player is None:
            raise ValueError("player")

        raise NotImplementedError()

    def new_turn_reset(self):
        pass

    def __str__(self):
        result = "PayAction("
        count = 0
        for resource in self._payItems:
            result += f"{resource.name}: {self._payItems[resource]}"
            count += 1
            if count != len(self._payItems):
                result += ", "
        result += ")"
        return result