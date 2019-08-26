from __future__ import annotations

from common.entities.dwarf import Dwarf
from common.entities.player import Player
from core.baseClasses.base_action import BaseAction
from core.containers.resource_container import ResourceContainer


class TakeAccumulatedItemsAction(BaseAction):
    def invoke(self, player: Player, active_card: ResourceContainer, current_dwarf: Dwarf) -> bool:
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

        result = player.give_resources(active_card.resources)
        active_card.clear_resources()
        return result

    def new_turn_reset(self):
        pass
