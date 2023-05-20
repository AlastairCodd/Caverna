from typing import Dict

from buisness_logic.actions.take_accumulated_items_action import TakeAccumulatedItemsAction
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.constants import card_ids
from core.enums.caverna_enums import ResourceTypeEnum


class WoodGatheringCard(BaseResourceContainingCard):
    def __init__(self) -> None:
        BaseResourceContainingCard.__init__(
            self, "Wood Gathering", card_ids.WoodGatheringCardId,
            actions=TakeAccumulatedItemsAction(False))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        newResources = {ResourceTypeEnum.wood: 1}
        self.give_resources(newResources)

        return self.resources
