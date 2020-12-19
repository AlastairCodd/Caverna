from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum
from core.containers.resource_container import ResourceContainer
from buisness_logic.actions import *


class DepotCard(BaseCard, ResourceContainer):

    def __init__(self):
        BaseCard.__init__(
            self, "Depot", 1,
            actions=take_accumulated_items_action.TakeAccumulatedItemsAction())
        ResourceContainer.__init__(self)

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        newResources = {
            ResourceTypeEnum.wood: 2,
            ResourceTypeEnum.ore: 2}
        self.give_resources(newResources)

        return self.resources
