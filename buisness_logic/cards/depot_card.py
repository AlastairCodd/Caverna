from typing import Dict

from buisness_logic.actions import *
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.constants import card_ids
from core.enums.caverna_enums import ResourceTypeEnum


class DepotCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Depot", card_ids.DepotCardId,
            actions=take_accumulated_items_action.TakeAccumulatedItemsAction())

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        newResources = {
            ResourceTypeEnum.wood: 1,
            ResourceTypeEnum.ore: 1}
        self.give_resources(newResources)

        return self.resources


class LargeDepotCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Large Depot", card_ids.LargeDepotCardId,
            actions=take_accumulated_items_action.TakeAccumulatedItemsAction())

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        amount_of_wood: int = 1 if self.has_resources else 2

        resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.wood: amount_of_wood,
            ResourceTypeEnum.stone: 1,
            ResourceTypeEnum.ore: 1}
        self.give_resources(resources)

        return self.resources
