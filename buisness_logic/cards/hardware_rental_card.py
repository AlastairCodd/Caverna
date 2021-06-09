from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.constants import card_ids
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from buisness_logic.actions import *


class HardwareRentalSmallCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Hardware Rental", card_ids.HardwareRentalSmallCardId,
            actions=Conditional(
                ActionCombinationEnum.AndThenOr,
                go_on_an_expedition_action.GoOnAnExpeditionAction(2),
                sow_action.SowAction()))


class HardwareRentalLargeCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Hardware Rental", card_ids.HardwareRentalLargeCardId,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                receive_action.ReceiveAction({ResourceTypeEnum.wood: 2}),
                Conditional(
                    ActionCombinationEnum.AndThenOr,
                    go_on_an_expedition_action.GoOnAnExpeditionAction(2),
                    sow_action.SowAction())))
