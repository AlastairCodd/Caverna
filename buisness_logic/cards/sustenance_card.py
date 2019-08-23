from typing import Dict

from buisness_logic.actions import takeAccumulatedItemsAction, placeATileAction
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ActionCombinationEnum, TileTypeEnum, ResourceTypeEnum


class SustenanceCard(BaseCard, ResourceContainer):

    def __init__(self):
        BaseCard.__init__(
            self, "Sustenance", 19,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
                placeATileAction.PlaceATileAction(TileTypeEnum.meadowFieldTwin)))
        ResourceContainer.__init__(self)

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        if self.has_resources:
            self.give_resource(ResourceTypeEnum.veg, 1)
        else:
            self.give_resource(ResourceTypeEnum.grain, 1)

        return self.resources