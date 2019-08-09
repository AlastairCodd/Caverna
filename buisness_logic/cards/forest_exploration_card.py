from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from core.containers.resource_container import ResourceContainer
from common.entities.multicombination import Combination
from buisness_logic.actions import *


class ForestExplorationCard(BaseCard, ResourceContainer):

    def __init__(self):
        BaseCard.__init__(
            self, "Forest Exploration", 6, -1,
            Combination(
                ActionCombinationEnum.AndThen,
                takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
                receiveAction.ReceiveAction({ResourceTypeEnum.food: 2})))
        ResourceContainer.__init__(self)

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        newResources = {ResourceTypeEnum.wood: 1} if self.has_resources() else {ResourceTypeEnum.wood: 2}
        self.give_resources(newResources)

        return self.get_resources()
