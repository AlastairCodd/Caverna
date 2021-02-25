from typing import Dict, cast

from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class OreMiningThreeCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Ore Mining", 14,
            actions=Conditional(
                ActionCombinationEnum.AndThenOr,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                receive_conditionally_action.ReceiveConditionallyAction(
                    self._condition,
                    {ResourceTypeEnum.ore: 1})))

    def _condition(self, player: BasePlayerRepository) -> int:
        if player is None:
            raise ValueError(str(player))
        tileContainer = cast(TileContainer, player)
        numberOfTiles = tileContainer.get_number_of_tiles_of_type(TileTypeEnum.oreMineDeepTunnelTwin)
        return numberOfTiles * 2

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        amount_of_ore: int = 1 if self.has_resources else 2
        self.give_resource(ResourceTypeEnum.ore, amount_of_ore)

        return self.resources


class OreMiningTwoCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Ore Mining", 14,
            actions=Conditional(
                ActionCombinationEnum.AndThenOr,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                receive_conditionally_action.ReceiveConditionallyAction(
                    self._condition,
                    {ResourceTypeEnum.ore: 1})))

    def _condition(self, player: BasePlayerRepository) -> int:
        if player is None:
            raise ValueError(str(player))
        tileContainer = cast(TileContainer, player)
        numberOfTiles = tileContainer.get_number_of_tiles_of_type(TileTypeEnum.oreMineDeepTunnelTwin)
        return numberOfTiles * 2

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        amount_of_ore: int = 2 if self.has_resources else 3
        self.give_resource(ResourceTypeEnum.ore, amount_of_ore)

        return self.resources
