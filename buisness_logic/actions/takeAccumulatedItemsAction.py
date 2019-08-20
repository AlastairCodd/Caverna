from __future__ import annotations
from common.entities.player import Player
from core.baseClasses.base_action import BaseAction
from core.containers.resource_container import ResourceContainer


class TakeAccumulatedItemsAction(BaseAction):
    def invoke(self, player: Player, active_card: ResourceContainer) -> bool:
        if player is None:
            raise ValueError("player")

        result = player.give_resources(active_card.resources)
        active_card.clear_resources()
        return result

    def new_turn_reset(self):
        pass

