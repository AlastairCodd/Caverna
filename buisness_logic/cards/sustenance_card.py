from typing import Dict

from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.constants import card_ids
from core.enums.caverna_enums import ActionCombinationEnum, TileTypeEnum, ResourceTypeEnum


class SustenanceVegAndGrainCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Sustenance", card_ids.SustenanceVegAndGrainCardId,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                place_a_twin_tile_action.PlaceATwinTileAction(TileTypeEnum.meadowFieldTwin)))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        if self.has_resources:
            self.give_resource(ResourceTypeEnum.veg, 1)
        else:
            self.give_resource(ResourceTypeEnum.grain, 1)

        return self.resources


class SustenanceGrainCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Sustenance", card_ids.SustenanceGrainCardId,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                Conditional(
                    ActionCombinationEnum.AndThen,
                    take_accumulated_items_action.TakeAccumulatedItemsAction(),
                    receive_action.ReceiveAction({ResourceTypeEnum.grain: 1})),
                place_a_twin_tile_action.PlaceATwinTileAction(TileTypeEnum.meadowFieldTwin)))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.food, 1)

        return self.resources
