from typing import Dict, Callable
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

    def invoke(self, player: Player, active_card: ResourceContainer) -> bool:
        if player is None:
            raise ValueError("player")

        condition: int = self._condition(player)
        result = True

        for _ in range(condition):
            result &= super().invoke(player, active_card)

        return result

    def new_turn_reset(self):
        pass
