from typing import Dict

from common.entities.dwarf import Dwarf
from common.entities.player import Player
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum
from core.baseClasses.base_action import BaseAction


class ReceiveAction(BaseAction):
    def __init__(self, receive_items: Dict[ResourceTypeEnum, int]):
        if receive_items is None:
            raise ValueError("receiveItems")
        self._receiveItems: Dict[ResourceTypeEnum, int] = receive_items

    def invoke(self, player: Player, active_card: ResourceContainer, current_dwarf: Dwarf) -> bool:
        if player is None:
            raise ValueError("player")

        return player.give_resources(self._receiveItems)

    def new_turn_reset(self):
        pass

    def __str__(self) -> str:
        result = "ReceiveAction("
        count = 0
        for resource in self._receiveItems:
            result += f"{resource.name}: {self._receiveItems[resource]}"
            count += 1
            if count != len(self._receiveItems):
                result += ", "
        result += ")"

        return result
