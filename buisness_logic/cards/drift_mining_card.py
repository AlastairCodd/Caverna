from typing import Dict
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.containers.resource_container import ResourceContainer
from common.entities.multicombination import Combination
from buisness_logic.actions import *


class DriftMiningCard(BaseCard, ResourceContainer):

    def __init__(self):
        BaseCard.__init__(
            self, "Drift Mining", 2, -1,
            Combination(
                ActionCombinationEnum.AndThen,
                takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
                placeATileAction.PlaceATileAction(TileTypeEnum.cavernTunnelTwin)))
        ResourceContainer.__init__(self)

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.stone, 2)

        return self.get_resources()
