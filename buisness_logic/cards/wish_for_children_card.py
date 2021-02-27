from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.constants import card_ids
from core.enums.caverna_enums import ActionCombinationEnum, TileTypeEnum, ResourceTypeEnum


class WishForChildrenCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Wish For Children", card_ids.WishForChildrenCardId, 2,
            Conditional(
                ActionCombinationEnum.EitherOr,
                get_a_baby_dwarf_action.GetABabyDwarfAction(),
                place_a_single_tile_action.PlaceASingleTileAction(TileTypeEnum.furnishedDwelling)
            )
        )


class UrgentWishForChildrenCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Urgent Wish For Children", card_ids.UrgentWishForChildrenCardId, 2,
            Conditional(
                ActionCombinationEnum.EitherOr,
                Conditional(
                    ActionCombinationEnum.AndThen,
                    get_a_baby_dwarf_action.GetABabyDwarfAction(),
                    place_a_single_tile_action.PlaceASingleTileAction(TileTypeEnum.furnishedDwelling)),
                receive_action.ReceiveAction({ResourceTypeEnum.coin: 3})
            )
        )