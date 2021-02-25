from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from buisness_logic.actions import *


class HardwareRentalSmallCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Hardware Rental", 9, -1,
            Conditional(
                ActionCombinationEnum.AndThenOr,
                go_on_an_expedition_action.GoOnAnExpeditionAction(2),
                sowAction.SowAction()))


class HardwareRentalLargeCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Hardware Rental", 9, -1,
            Conditional(
                ActionCombinationEnum.AndThenOr,
                receive_action.ReceiveAction({ResourceTypeEnum.wood: 2}),
                Conditional(
                    ActionCombinationEnum.AndThenOr,
                    go_on_an_expedition_action.GoOnAnExpeditionAction(2),
                    sowAction.SowAction())))
