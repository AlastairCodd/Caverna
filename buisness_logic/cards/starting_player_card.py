from typing import Dict

from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum
from core.containers.resource_container import ResourceContainer
from buisness_logic.actions import *


class StartingPlayerCard(BaseCard, ResourceContainer):

    def __init__(self):
        BaseCard.__init__(
            self, "Starting Player", 17,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
                Conditional(
                    ActionCombinationEnum.AndThen,
                    becomeStartingPlayerAction.BecomeStartingPlayerAction(),
                    receiveAction.ReceiveAction({ResourceTypeEnum.ruby: 1}))))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.food, 1)

        return self.resources
