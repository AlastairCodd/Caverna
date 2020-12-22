from typing import Dict
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.containers.resource_container import ResourceContainer
from buisness_logic.actions import *


class ClearingCard(BaseCard, ResourceContainer):

    def __init__(self):
        BaseCard.__init__(
            self, "Clearing", 0,
            actions=Conditional(
                ActionCombinationEnum.AndThenOr,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                place_a_twin_tile_action.PlaceATwinTileAction(TileTypeEnum.meadowFieldTwin)))
        ResourceContainer.__init__(self)

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resource(ResourceTypeEnum.wood, 2)

        return self.resources
