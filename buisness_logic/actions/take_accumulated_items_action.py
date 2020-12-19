from __future__ import annotations

from buisness_logic.actions.base_receive_action import BaseReceiveAction
from common.entities.dwarf import Dwarf
from core.repositories.base_player_repository import BasePlayerRepository
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_card import BaseCard
from core.containers.resource_container import ResourceContainer


class TakeAccumulatedItemsAction(BaseReceiveAction):
    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        """Moves the resources from the active card to the player.

        :param player: The player who will receive the items. This cannot be null.
        :param active_card: The card which is providing the items. This cannot be null.
        :param current_dwarf: Unused.
        :return: A result lookup indicating the success of the action, and the number of resources which were taken.
            This will never be null.
        """
        if player is None:
            raise ValueError("Player cannot be null.")
        if active_card is None:
            raise ValueError("Active Card cannot be null.")
        if not isinstance(active_card, ResourceContainer):
            raise ValueError("Active Card must be a resource container")

        result: ResultLookup[int] = self._give_player_resources(player, active_card.resources)
        active_card.clear_resources()

        return result

    def new_turn_reset(self):
        pass