from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ActionCombinationEnum, TileTypeEnum


class SlashAndBurnCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Slash and Burn", 15,
            actions=Conditional(
                ActionCombinationEnum.AndThenOr,
                placeATileAction.PlaceATileAction(TileTypeEnum.meadowFieldTwin),
                sowAction.SowAction()
            ))