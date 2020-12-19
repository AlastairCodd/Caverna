from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum


class GrowthCard(BaseCard):

    def __init__(self):
        BaseCard.__init__(
            self, "Growth", 7,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                receive_action.ReceiveAction({
                    ResourceTypeEnum.wood: 1,
                    ResourceTypeEnum.stone: 1,
                    ResourceTypeEnum.ore: 1,
                    ResourceTypeEnum.food: 1,
                    ResourceTypeEnum.coin: 2}),
                get_a_baby_dwarf_action.GetABabyDwarfAction()))
