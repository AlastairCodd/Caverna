from buisness_logic.actions.receive_action import ReceiveAction
from buisness_logic.actions.weekly_market_action import WeeklyMarketAction
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.constants import card_ids
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum


class WeeklyMarketCard(BaseCard):

    def __init__(self):
        BaseCard.__init__(
            self, "Weekly Market", card_ids.WeeklyMarketCardId,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                ReceiveAction({ResourceTypeEnum.coin: 4}),
                WeeklyMarketAction()))
