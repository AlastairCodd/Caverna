from typing import Dict

from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.containers.resource_container import ResourceContainer
from buisness_logic.actions import *


class FenceBuildingCard(BaseCard, ResourceContainer):

    def __init__(self):
        BaseCard.__init__(
            self, "Fence Building", 5,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
                Conditional(
                    ActionCombinationEnum.AndOr,
                    Conditional(
                        ActionCombinationEnum.AndThen,
                        payAction.PayAction({ResourceTypeEnum.wood: 2}),
                        placeATileAction.PlaceATileAction(TileTypeEnum.pastureTwin)),
                    Conditional(
                        ActionCombinationEnum.AndThen,
                        payAction.PayAction({ResourceTypeEnum.wood: 4}),
                        placeATileAction.PlaceATileAction(TileTypeEnum.pastureTwin)))))
        ResourceContainer.__init__(self)

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        newResources = {ResourceTypeEnum.wood: 1} if self.has_resources else {ResourceTypeEnum.wood: 2}
        self.give_resources(newResources)

        return self.resources
