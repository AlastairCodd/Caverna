from typing import Dict

from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from core.containers.resource_container import ResourceContainer
from buisness_logic.actions import *


class LoggingCard(BaseCard, ResourceContainer):

    def __init__(self):
        BaseCard.__init__(
            self, "Logging", 13,
            actions=Conditional(
                ActionCombinationEnum.AndThenOr,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                go_on_an_expedition_action.GoOnAnExpeditionAction(1)))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.wood, 3)

        return self.resources
