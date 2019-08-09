from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from buisness_logic.actions import *


class OreMineConstructionCard(BaseCard):

    def __init__(self):
        BaseCard.__init__(
            self, "Ore Mine Construction", 22, 1,
            Conditional(
                ActionCombinationEnum.AndThenOr,
                Conditional(
                    ActionCombinationEnum.AndThen,
                    placeATileAction.PlaceATileAction(TileTypeEnum.oreMineDeepTunnelTwin),
                    receiveAction.ReceiveAction({ResourceTypeEnum.ore: 3})),
                goOnAnExpeditionAction.GoOnAnExpeditionAction(3)))
