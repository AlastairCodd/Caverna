from typing import Dict
from core.enums.caverna_enums import ResourceTypeEnum
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_action import BaseAction
from common.entities.player import Player

class BecomeStartingPlayerAction(BaseAction):
    def Invoke(
        self,
        player: Player,
        activeCard: BaseCard ) -> bool:
        if player is None:
            raise ValueException("player")
        
        raise NotImplementedError()
        