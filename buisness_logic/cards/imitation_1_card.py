from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from common.entities.multicombination import Combination
from buisness_logic.actions import *


class Imitation1Card(BaseCard):

    def __init__(self):
        BaseCard.__init__(
            self, "Imitation", 10, -1,
            Combination(
                ActionCombinationEnum.AndThen,
                payAction.PayAction({ResourceTypeEnum.food: 1}),
                useAnotherCardAction.UseAnotherCardAction()))
