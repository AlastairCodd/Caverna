from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.constants import card_ids
from core.enums.caverna_enums import ActionCombinationEnum, TileTypeEnum, ResourceTypeEnum
from core.errors.invalid_operation_error import InvalidOperationError


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

    def hide_card(self) -> None:
        if not self._is_visible:
            raise InvalidOperationError("Cannot hide a card that is not visible")
        self._is_visible = False


class UrgentWishForChildrenCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Urgent Wish For Children", card_ids.UrgentWishForChildrenCardId, 2,
            Conditional(
                ActionCombinationEnum.EitherOr,
                Conditional(
                    ActionCombinationEnum.AndThen,
                    place_a_single_tile_action.PlaceASingleTileAction(TileTypeEnum.furnishedDwelling),
                    get_a_baby_dwarf_action.GetABabyDwarfAction()),
                receive_action.ReceiveAction({ResourceTypeEnum.coin: 3})
            )
        )