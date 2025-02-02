from typing import Dict

from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.constants import card_ids
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum


class FenceBuildingSmallCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Fence Building", card_ids.FenceBuildingSmallCardId,
            actions=Conditional(
                ActionCombinationEnum.AndThenOr,
                take_accumulated_items_action.TakeAccumulatedItemsAction(False),
                place_fences_action.PlaceFencesAction()))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.wood, 1)

        return self.resources


class FenceBuildingLargeCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Fence Building", card_ids.FenceBuildingLargeCardId,
            actions=Conditional(
                ActionCombinationEnum.AndThenOr,
                take_accumulated_items_action.TakeAccumulatedItemsAction(False),
                place_fences_action.PlaceFencesAction()))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        amount_of_wood: int = 1 if self.has_resources else 2
        self.give_resource(ResourceTypeEnum.wood, amount_of_wood)

        return self.resources
