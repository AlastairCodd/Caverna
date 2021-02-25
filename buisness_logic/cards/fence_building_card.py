from typing import Dict

from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum


class FenceBuildingSmallCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Fence Building", 5,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                Conditional(
                    ActionCombinationEnum.AndOr,
                    place_a_single_tile_action.PlaceASingleTileAction(TileTypeEnum.pasture),
                    place_a_twin_tile_action.PlaceATwinTileAction(TileTypeEnum.pastureTwin))))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.wood, 1)

        return self.resources


class FenceBuildingLargeCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Fence Building", 5,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                Conditional(
                    ActionCombinationEnum.AndOr,
                    place_a_single_tile_action.PlaceASingleTileAction(TileTypeEnum.pasture),
                    place_a_twin_tile_action.PlaceATwinTileAction(TileTypeEnum.pastureTwin))))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        amount_of_wood: int = 1 if self.has_resources else 2
        self.give_resource(ResourceTypeEnum.wood, amount_of_wood)

        return self.resources
