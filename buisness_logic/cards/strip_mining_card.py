from typing import Dict

from buisness_logic.actions.receive_action import ReceiveAction
from buisness_logic.actions.take_accumulated_items_action import TakeAccumulatedItemsAction
from common.entities.multiconditional import Conditional
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.enums.caverna_enums import ActionCombinationEnum, ResourceTypeEnum


class StripMiningCard(BaseResourceContainingCard):
    def __init__(self) -> None:
        BaseResourceContainingCard.__init__(
            self, "Strip Mining", 38,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                TakeAccumulatedItemsAction(),
                ReceiveAction({ResourceTypeEnum.wood: 2})
            ))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        new_resources = {ResourceTypeEnum.stone: 1} if self.has_resources else {ResourceTypeEnum.ore: 1}
        self.give_resources(new_resources)

        return self.resources