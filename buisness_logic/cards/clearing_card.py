from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.containers.resource_container import ResourceContainer
from common.entities.multicombination import Combination
from buisness_logic.actions import *


class ClearingCard(ResourceContainer, BaseCard):

    def __init__(self):
        BaseCard.__init__(
            self, "Clearing", 0, -1,
            Combination(
                ActionCombinationEnum.AndThenOr,
                takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
                placeATileAction.PlaceATileAction(TileTypeEnum.meadowFieldTwin)))
        ResourceContainer.__init__(self)

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.wood, 2)

        return self.get_resources()
