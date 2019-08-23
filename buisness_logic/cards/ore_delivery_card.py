from typing import Dict

from buisness_logic.actions import takeAccumulatedItemsAction
from core.baseClasses.base_card import BaseCard
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ResourceTypeEnum


class OreDeliveryCard(BaseCard, ResourceContainer):

    def __init__(self):
        BaseCard.__init__(
            self, "Ore Delivery", 30, 3,
            actions=takeAccumulatedItemsAction.TakeAccumulatedItemsAction())
        ResourceContainer.__init__(self)

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resources(
            {ResourceTypeEnum.stone: 1,
             ResourceTypeEnum.ore: 1})

        return self.resources
