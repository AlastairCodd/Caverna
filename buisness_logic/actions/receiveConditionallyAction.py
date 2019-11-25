from typing import Dict, Callable, List

from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum
from common.entities.player import Player
from buisness_logic.actions.receiveAction import ReceiveAction


class ReceiveConditionallyAction(ReceiveAction):
    def __init__(self, condition: Callable[[Player], int], receive_items: Dict[ResourceTypeEnum, int]):
        if condition is None:
            raise ValueError("condition")
        self._condition = condition
        ReceiveAction.__init__(self, receive_items)

    def invoke(self, player: Player, active_card: BaseCard, current_dwarf: Dwarf) -> ResultLookup[int]:
        """Gives the player some items proportional to how many times they fulfil the given condition.

        :param player: The player who will receive items. This cannot be null.
        :param active_card: Unused
        :param current_dwarf: Unused
        :return: True if they successfully received the items, false if not. 
        """
        if player is None:
            raise ValueError("player")

        number_of_times_to_give: int = self._condition(player)
        success: bool = True
        count: int = 0
        errors: List[str] = []

        for _ in range(number_of_times_to_give):
            received_result: ResultLookup[int] = super().invoke(player, active_card, current_dwarf)
            success &= received_result.flag
            count += received_result.value
            for error in received_result.errors:
                errors.append(error)

        result: ResultLookup[int] = ResultLookup(success, count, errors)
        return result

    def new_turn_reset(self):
        pass
