from typing import Dict, cast

from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from common.entities.player import Player
from core.baseClasses.base_card import BaseCard
from core.containers.resource_container import ResourceContainer
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum


class OreMiningCard(BaseCard, ResourceContainer):

    def __init__(self):
        BaseCard.__init__(
            self, "Ore Mining", 14,
            actions=Conditional(
                ActionCombinationEnum.AndThenOr,
                takeAccumulatedItemsAction.TakeAccumulatedItemsAction(),
                receiveConditionallyAction.ReceiveConditionallyAction(
                    self._condition,
                    {ResourceTypeEnum.ore: 1})))
        ResourceContainer.__init__(self)

    def _condition(self, player: Player) -> int:
        if player is None:
            raise ValueError(str(player))
        tileContainer = cast(TileContainer, player)
        numberOfTiles = tileContainer.get_number_of_tiles_of_type(TileTypeEnum.oreMineDeepTunnelTwin)
        return numberOfTiles * 2

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        if self.has_resources:
            newResources = {ResourceTypeEnum.ore: 2}
        else:
            newResources = {ResourceTypeEnum.ore: 3}
        self.give_resources(newResources)

        return self.resources
