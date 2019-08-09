from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from common.entities.multicombination import Combination
from buisness_logic.actions import *


class HouseworkCard(BaseCard):

    def __init__(self):
        BaseCard.__init__(
            self,
            "Housework", 8, -1,
            Combination(
                ActionCombinationEnum.AndOr,
                receiveAction.ReceiveAction({ResourceTypeEnum.dog: 1}),
                placeATileAction.PlaceATileAction(TileTypeEnum.furnishedCavern)))
