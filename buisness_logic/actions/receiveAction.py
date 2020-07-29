from typing import Dict

from common.entities.dwarf import Dwarf
from core.repositories.base_player_repository import BasePlayerRepository
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum
from core.baseClasses.base_action import BaseAction


class ReceiveAction(BaseAction):
    def __init__(self, receive_items: Dict[ResourceTypeEnum, int]):
        if receive_items is None:
            raise ValueError("receiveItems")
        self._receiveItems: Dict[ResourceTypeEnum, int] = receive_items

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        """Gives the player a static quantity of resources.

        :param player: The player to receive the resources. This cannot be null.
        :param active_card: Unused.
        :param current_dwarf: Unused.
        :return: A result lookup indicating the success of the action, and the number of resources which were given.
            This will never be null.
        """
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
