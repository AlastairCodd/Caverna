from typing import Dict

from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.constants import card_ids
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum


class ForestExplorationFoodCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Forest Exploration", card_ids.ForestExplorationFoodCardId,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                take_accumulated_items_action.TakeAccumulatedItemsAction(False),
                receive_action.ReceiveAction({ResourceTypeEnum.food: 2})))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        amount_of_wood: int = 1 if self.has_resources else 2
        self.give_resource(ResourceTypeEnum.wood, amount_of_wood)

        return self.resources


class ForestExplorationVegCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Forest Exploration", card_ids.ForestExplorationVegCardId,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                take_accumulated_items_action.TakeAccumulatedItemsAction(False),
                receive_action.ReceiveAction({ResourceTypeEnum.veg: 1})))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.wood, 1)

        return self.resources
