from buisness_logic.actions import convert_single_action
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.constants import card_ids
from core.enums.caverna_enums import ActionCombinationEnum, ResourceTypeEnum


class OreTradingCard(BaseCard):

    def __init__(self):
        BaseCard.__init__(
            self, "Ore Trading", card_ids.OreTradingCardId, 4,
            actions=Conditional(
                ActionCombinationEnum.Or,
                convert_single_action.ConvertSingleAction(
                    {ResourceTypeEnum.ore: 2},
                    {ResourceTypeEnum.coin: 2, ResourceTypeEnum.food: 1},
                    1),
                Conditional(
                    ActionCombinationEnum.Or,
                    convert_single_action.ConvertSingleAction(
                        {ResourceTypeEnum.ore: 2},
                        {ResourceTypeEnum.coin: 2, ResourceTypeEnum.food: 1},
                        2),
                    convert_single_action.ConvertSingleAction(
                        {ResourceTypeEnum.ore: 2},
                        {ResourceTypeEnum.coin: 2, ResourceTypeEnum.food: 1},
                        3))))
