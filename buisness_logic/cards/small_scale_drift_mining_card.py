from buisness_logic.actions import placeATileAction, receiveAction
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ActionCombinationEnum, ResourceTypeEnum, TileTypeEnum


class SmallScaleDriftMiningCard(BaseCard):

    def __init__(self):
        BaseCard.__init__(
            self, "Small Scale Drift Mining", 13,
            actions=Conditional(
                ActionCombinationEnum.AndOr,
                receiveAction.ReceiveAction({ResourceTypeEnum.stone: 1}),
                placeATileAction.PlaceATileAction(TileTypeEnum.cavern)))
