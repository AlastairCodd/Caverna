from typing import Dict

from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.constants import card_ids
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum


class DriftMiningTwoStoneCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Drift Mining", card_ids.DriftMiningTwoStoneCardId,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                place_a_twin_tile_action.PlaceATwinTileAction(TileTypeEnum.cavernTunnelTwin)))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.stone, 2)

        return self.resources


class DriftMiningOneStoneCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Drift Mining", card_ids.DriftMiningOneStoneCardId,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                place_a_twin_tile_action.PlaceATwinTileAction(TileTypeEnum.cavernTunnelTwin)))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.stone, 1)

        return self.resources
