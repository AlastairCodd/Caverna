from buisness_logic.actions.get_a_baby_dwarf_action import GetABabyDwarfAction
from buisness_logic.actions.placeATileAction import PlaceATileAction
from buisness_logic.actions.receive_action import ReceiveAction
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ActionCombinationEnum, TileTypeEnum, ResourceTypeEnum


class WishForChildrenCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Wish For Children", 27, 2,
            Conditional(
                ActionCombinationEnum.EitherOr,
                GetABabyDwarfAction(),
                PlaceATileAction(TileTypeEnum.furnishedDwelling)
            )
        )


class UrgentWishForChildrenCard(BaseCard):
    def __init__(self):
        BaseCard.__init__(
            self, "Urgent Wish For Children", 28, 2,
            Conditional(
                ActionCombinationEnum.EitherOr,
                Conditional(
                    ActionCombinationEnum.AndThen,
                    GetABabyDwarfAction(),
                    PlaceATileAction(TileTypeEnum.furnishedDwelling)),
                ReceiveAction({ResourceTypeEnum.coin: 3})
            )
        )