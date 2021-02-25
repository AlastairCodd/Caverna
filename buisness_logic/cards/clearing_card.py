from typing import Dict
from common.entities.multiconditional import Conditional
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from buisness_logic.actions import *


class ClearingCard(BaseResourceContainingCard):
    def __init__(self, amount_of_wood: int):
        if amount_of_wood < 0:
            raise ValueError("Amount of wood must be positive")
        self._amount_of_wood: int = amount_of_wood
        BaseResourceContainingCard.__init__(
            self, "Clearing", 0,
            actions=Conditional(
                ActionCombinationEnum.AndThenOr,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                place_a_twin_tile_action.PlaceATwinTileAction(TileTypeEnum.meadowFieldTwin)))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.wood, self._amount_of_wood)

        return self.resources
