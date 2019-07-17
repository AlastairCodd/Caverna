from typing import Dict
from common.entities.player import Player
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard

class PayAction(BaseAction):
    _payItems = Dict[ResourceTypeEnum, int]
        
    def __init__(self, payItems: Dict[ResourceTypeEnum, int]):
        if payItems is None:
            raise ValueException("payItems")
        self._payItems = payItems
    
    def Invoke(
        self,
        player: Player,
        activeCard: BaseCard ) -> bool:
        if player is None:
            raise ValueException("player")
        
        raise NotImplementedError()