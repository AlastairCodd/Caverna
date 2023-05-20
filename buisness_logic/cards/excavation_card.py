from typing import Dict

from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.constants import card_ids
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum


class ExcavationTwoCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Excavation", card_ids.ExcavationTwoStoneCardId,
            actions=Conditional(
                ActionCombinationEnum.OrAndThenStrict,
                take_accumulated_items_action.TakeAccumulatedItemsAction(False),
                Conditional(
                    ActionCombinationEnum.Or,
                    place_a_twin_tile_action.PlaceATwinTileAction(TileTypeEnum.cavernTunnelTwin),
                    place_a_twin_tile_action.PlaceATwinTileAction(TileTypeEnum.cavernCavernTwin))))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        newResources = {ResourceTypeEnum.stone: 1} if self.has_resources else {ResourceTypeEnum.stone: 2}
        self.give_resources(newResources)

        return self.resources


class ExcavationOneCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Excavation", card_ids.ExcavationOneStoneCardId,
            actions=Conditional(
                ActionCombinationEnum.OrAndThenStrict,
                take_accumulated_items_action.TakeAccumulatedItemsAction(False),
                Conditional(
                    ActionCombinationEnum.Or,
                    place_a_twin_tile_action.PlaceATwinTileAction(TileTypeEnum.cavernTunnelTwin),
                    place_a_twin_tile_action.PlaceATwinTileAction(TileTypeEnum.cavernCavernTwin))))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resources({ResourceTypeEnum.stone: 1})

        return self.resources
