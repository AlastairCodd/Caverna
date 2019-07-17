from typing import Dict, Callable
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum
from common.entities.player import Player
from buisness_logic.actions.receiveAction import ReceiveAction

class ReceiveConditionallyAction(ReceiveAction):
    _condition: Callable[[Player, BaseCard], bool]

    def __init__(
        self, 
        condition: Callable[[Player, BaseCard], bool], 
        receiveItems: Dict[ResourceTypeEnum, int]):
        if condition is None:
            raise ValueError("condition")
        self._condition = condition
        super(ReceiveConditionallyAction, self).__init__(receiveItems)

    def Invoke(
        self,
        player: Player,
        activeCard: BaseCard ) -> bool:
        if player is None:
            raise ValueError("player")
        if activeCard is None:
            raise ValueError("activeCard")
        
        if self._condition(player, activeCard):
            return super(ReceiveConditionallyAction, self).Invoke(player, activeCard)
        return False