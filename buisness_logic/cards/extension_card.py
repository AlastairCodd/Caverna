from buisness_logic.actions.place_a_twin_tile_action import PlaceATwinTileAction
from buisness_logic.actions.receive_action import ReceiveAction
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.constants import card_ids
from core.enums.caverna_enums import ActionCombinationEnum, TileTypeEnum, ResourceTypeEnum


class ExtensionCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Extension", card_ids.ExtensionCardId,
            actions=Conditional(
                ActionCombinationEnum.EitherOr,
                Conditional(
                    ActionCombinationEnum.AndThen,
                    PlaceATwinTileAction(TileTypeEnum.meadowFieldTwin),
                    ReceiveAction({ResourceTypeEnum.wood: 1})),
                Conditional(
                    ActionCombinationEnum.AndThen,
                    PlaceATwinTileAction(TileTypeEnum.cavernTunnelTwin),
                    ReceiveAction({ResourceTypeEnum.stone: 1}))
            )
        )