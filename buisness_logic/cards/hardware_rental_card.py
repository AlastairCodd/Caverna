from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from common.entities.multicombination import Combination
from buisness_logic.actions import *


class HardwareRentalCard(BaseCard):

    def __init__(self):
        BaseCard.__init__(
            self, "Hardware Rental", 9, -1,
            Combination(
                ActionCombinationEnum.AndThenOr,
                receiveAction.ReceiveAction({ResourceTypeEnum.wood: 2}),
                Combination(
                    ActionCombinationEnum.AndThenOr,
                    goOnAnExpeditionAction.GoOnAnExpeditionAction(2),
                    sowAction.SowAction())))
