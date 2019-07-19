from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from common.entities.player import Player

class GetABabyDwarfAction(BaseAction):
    def invoke(
        self,
        player: Player,
        activeCard: BaseCard ) -> bool:
        if player is None:
            raise ValueException("player")
        raise NotImplementedException
        