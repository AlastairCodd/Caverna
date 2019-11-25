from __future__ import annotations

from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.containers.resource_container import ResourceContainer


class TakeAccumulatedItemsAction(BaseAction):
    def invoke(self, player: Player, active_card: BaseCard, current_dwarf: Dwarf) -> ResultLookup[int]:
        """Moves the resources from the active card to the player.

        :param player: The player who will receive the items. This cannot be null.
        :param active_card: The card which is providing the items. This cannot be null.
        :param current_dwarf: Unused.
        :return:
        """
        if player is None:
            raise ValueError("Player cannot be null.")
        if active_card is None:
            raise ValueError("Active Card cannot be null.")
        if not isinstance(active_card, ResourceContainer):
            raise ValueError("Active Card must be a resource container")

        amount: int = sum(active_card.resources.values())
        success: bool = player.give_resources(active_card.resources)
        active_card.clear_resources()

        result: ResultLookup[int] = ResultLookup(success, amount)
        return result

    def new_turn_reset(self):
        pass
