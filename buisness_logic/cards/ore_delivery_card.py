from typing import Dict

from buisness_logic.actions import take_accumulated_items_action
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.constants import card_ids
from core.enums.caverna_enums import ResourceTypeEnum


class OreDeliveryCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Ore Delivery", card_ids.OreDeliveryCardId, 3,
            take_accumulated_items_action.TakeAccumulatedItemsAction())

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resources(
            {ResourceTypeEnum.stone: 1,
             ResourceTypeEnum.ore: 1})

        return self.resources
