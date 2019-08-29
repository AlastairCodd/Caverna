from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from buisness_logic.actions import *


class HouseworkCard(BaseCard):

    def __init__(self):
        BaseCard.__init__(
            self, "Housework", 8, -1,
            Conditional(
                ActionCombinationEnum.AndOr,
                receiveAction.ReceiveAction({ResourceTypeEnum.dog: 1}),
                placeATileAction.PlaceATileAction(TileTypeEnum.furnishedCavern)))
