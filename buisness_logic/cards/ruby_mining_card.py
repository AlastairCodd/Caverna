from typing import Dict

from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from core.containers.resource_container import ResourceContainer
from buisness_logic.actions import *


class RubyMiningCard(BaseCard, ResourceContainer):

    def __init__(self):
        BaseCard.__init__(
            self, "Ruby Mining", 33, 4,
            Conditional(
                ActionCombinationEnum.AndThenOr,
                takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
                buyFromMarketAction.BuyFromMarketAction()))
        ResourceContainer.__init__(self)

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        newResources = {ResourceTypeEnum.ruby: 1} if self.has_resources else {ResourceTypeEnum.ruby: 2}
        self.give_resources(newResources)

        return self.resources
