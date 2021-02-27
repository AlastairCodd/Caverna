from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.constants import card_ids
from core.enums.caverna_enums import ActionCombinationEnum, ResourceTypeEnum, TileTypeEnum


class SmallScaleDriftMiningCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Small Scale Drift Mining", card_ids.SmallScaleDriftMiningCardId,
            actions=Conditional(
                ActionCombinationEnum.AndOr,
                receive_action.ReceiveAction({ResourceTypeEnum.stone: 1}),
                place_a_twin_tile_action.PlaceATwinTileAction(TileTypeEnum.cavernTunnelTwin)))
