from typing import Dict, Callable

from common.entities.dwarf import Dwarf
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum
from common.entities.player import Player
from buisness_logic.actions.receiveAction import ReceiveAction


class ReceiveConditionallyAction(ReceiveAction):
    def __init__(self, condition: Callable[[Player], int], receive_items: Dict[ResourceTypeEnum, int]):
        if condition is None:
            raise ValueError("condition")
        self._condition = condition
        ReceiveAction.__init__(self, receive_items)

    def invoke(self, player: Player, active_card: ResourceContainer, current_dwarf: Dwarf) -> bool:
        """Gives the player some items proportional to how many times they fulfil the given condition.

        :param player: The player who will receive items. This cannot be null.
        :param active_card: Unused
        :param current_dwarf: Unused
        :return: True if they successfully received the items, false if not. 
        """
        if player is None:
            raise ValueError("player")

        condition: int = self._condition(player)
        result = True

        for _ in range(condition):
            result &= super().invoke(player, active_card, current_dwarf)

        return result

    def new_turn_reset(self):
        pass
