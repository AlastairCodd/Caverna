from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from common.entities.multicombination import Combination
from buisness_logic.actions import *

class WeeklyMarketCard(BaseCard):
    
    def __init__(self):
        self._name = "Weekly Market"
        self._id = 20
        self._level = -1
        self._actions = Combination(
            ActionCombinationEnum.AndThenOr,
            receiveAction.ReceiveAction( {ResourceTypeEnum.coin, 4} ),
            buyFromMarketAction.BuyFromMarketAction() )