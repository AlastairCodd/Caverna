from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from common.entities.player import Player

class BuyFromMarketAction(BaseAction):
    def Invoke(
        self,
        player: Player,
        activeCard: BaseCard ) -> bool:
        if player is None:
            raise ValueException("player")
        raise NotImplementedException
        