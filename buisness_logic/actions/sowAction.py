from common.entities.player import Player
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard

class SowAction(BaseAction):

    def Invoke(
        self,
        player: Player,
        activeCard: BaseCard ) -> bool:
        if player is None:
            raise ValueException("player")
        
        raise NotImplementedError()