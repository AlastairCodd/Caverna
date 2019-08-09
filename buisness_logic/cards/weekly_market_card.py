from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from buisness_logic.actions import *


class WeeklyMarketCard(BaseCard):

    def __init__(self):
        BaseCard.__init__(
            self, "Weekly Market", 20,
            actions=Conditional(
                ActionCombinationEnum.AndThenOr,
                receiveAction.ReceiveAction({ResourceTypeEnum.coin: 4}),
                buyFromMarketAction.BuyFromMarketAction()))
