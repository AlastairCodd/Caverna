from typing import Dict

from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.constants import card_ids
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum


class SheepFarmingCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Sheep Farming", card_ids.SheepFarmingCardId, 1,
            actions=Conditional(
                ActionCombinationEnum.AndThenOr,
                place_fences_action.PlaceFencesAndStableAction(),
                take_accumulated_items_action.TakeAccumulatedItemsAction(True)))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.sheep, 1)

        return self.resources
