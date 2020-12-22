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
                receive_action.ReceiveAction({ResourceTypeEnum.dog: 1}),
                place_a_single_tile_action.PlaceASingleTileAction(TileTypeEnum.furnishedCavern)))
