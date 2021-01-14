from typing import Dict

from buisness_logic.actions.base_receive_action import BaseReceiveAction
from buisness_logic.services.base_receive_event_service import BaseReceiveEventService
from common.entities.dwarf import Dwarf
from core.baseClasses.base_action import BaseAction
from core.repositories.base_player_repository import BasePlayerRepository
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum


class ReceiveAction(BaseReceiveAction):
    def __init__(self, items_to_receive: Dict[ResourceTypeEnum, int]) -> None:
        BaseReceiveAction.__init__(self, items_to_receive)

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
            raise ValueError("Player cannot be none")

        result: ResultLookup[int] = self._give_player_resources(player, self._items_to_receive)
        return result

    def new_turn_reset(self):
        pass

    def __str__(self) -> str:
        result = "ReceiveAction("
        count = 0
        for resource in self._items_to_receive:
            result += f"{resource.name}: {self._items_to_receive[resource]}"
            count += 1
            if count != len(self._items_to_receive):
                result += ", "
        result += ")"

        return result
