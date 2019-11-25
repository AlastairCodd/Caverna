from typing import Dict

from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum
from core.baseClasses.base_action import BaseAction


class ReceiveAction(BaseAction):
    def __init__(self, receive_items: Dict[ResourceTypeEnum, int]):
        if receive_items is None:
            raise ValueError("receiveItems")
        self._receiveItems: Dict[ResourceTypeEnum, int] = receive_items

    def invoke(self, player: Player, active_card: BaseCard, current_dwarf: Dwarf) -> ResultLookup[int]:
        if player is None:
            raise ValueError("player")

        result: ResultLookup[int]
        if player.give_resources(self._receiveItems):
            result = ResultLookup(True, sum(self._receiveItems.values()))
        else:
            result = ResultLookup(False, 0)
        return result

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
