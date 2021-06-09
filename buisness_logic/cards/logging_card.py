from typing import Dict

from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.constants import card_ids
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum


class LoggingOneCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Logging", card_ids.LoggingOneCardId,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                go_on_an_expedition_action.GoOnAnExpeditionAction(1)))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.wood, 3)

        return self.resources


class LoggingThreeCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Logging", card_ids.LoggingThreeCardId,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                go_on_an_expedition_action.GoOnAnExpeditionAction(1)))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        amount: int = 1 if self.has_resources else 3
        self.give_resource(ResourceTypeEnum.wood, amount)

        return self.resources
