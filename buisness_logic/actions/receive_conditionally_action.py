from typing import Dict, Callable, List

from buisness_logic.actions.base_receive_action import BaseReceiveAction
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class ReceiveConditionallyAction(BaseReceiveAction):
    def __init__(
            self,
            condition: Callable[[BasePlayerRepository], int],
            receive_items: Dict[ResourceTypeEnum, int]) -> None:
        if condition is None:
            raise ValueError("Condition cannot be null")
        if receive_items is None:
            raise ValueError("Receive Items cannot be none")

        self._condition: Callable[[BasePlayerRepository], int] = condition
        self._receive_items: Dict[ResourceTypeEnum, int] = receive_items
        BaseReceiveAction.__init__(self)

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        """Gives the player some items proportional to how many times they fulfil the given condition.

        :param player: The player who will receive items. This cannot be null.
        :param active_card: Unused
        :param current_dwarf: Unused
        :return: A result lookup indicating the success of the action, and the number of resources which were given.
            This will never be null.
        """
        if player is None:
            raise ValueError("player")

        number_of_times_to_give: int = self._condition(player)

        resources_to_give: Dict[ResourceTypeEnum, int] = {r: self._receive_items[r] * number_of_times_to_give for r in self._receive_items}

        result: ResultLookup[int] = self._give_player_resources(player, resources_to_give)
        return result

    def new_turn_reset(self) -> None:
        pass

    def __str__(self) -> str:
        result = "ReceiveAction("
        count = 0
        for resource in self._receive_items:
            result += f"{resource.name}: {self._receive_items[resource]}"
            count += 1
            if count != len(self._receive_items):
                result += ", "
        result += ")"

        return result

