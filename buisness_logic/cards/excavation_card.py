from typing import Dict

from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.containers.resource_container import ResourceContainer
from buisness_logic.actions import *


class ExcavationCard(BaseCard, ResourceContainer):

    def __init__(self):
        BaseCard.__init__(
            self, "Excavation", 4,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                Conditional(
                    ActionCombinationEnum.Or,
                    place_a_twin_tile_action.PlaceATwinTileAction(TileTypeEnum.cavernTunnelTwin),
                    place_a_twin_tile_action.PlaceATwinTileAction(TileTypeEnum.cavernCavernTwin))))
        ResourceContainer.__init__(self)

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        newResources = {ResourceTypeEnum.stone: 1} if self.has_resources else {ResourceTypeEnum.stone: 2}
        self.give_resources(newResources)

        return self.resources
