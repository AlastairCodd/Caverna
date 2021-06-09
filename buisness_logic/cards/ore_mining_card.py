from abc import ABCMeta
from typing import Dict, cast

from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.constants import card_ids
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class BaseOreMiningCard(BaseResourceContainingCard, metaclass=ABCMeta):
    def __init__(
            self,
            tile_id: int) -> None:
        BaseResourceContainingCard.__init__(
            self, "Ore Mining", tile_id,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                receive_conditionally_action.ReceiveConditionallyAction(
                    self._condition,
                    {ResourceTypeEnum.ore: 1}
                )))

    def _condition(self, player: BasePlayerRepository) -> int:
        if player is None:
            raise ValueError(str(player))
        tile_container = cast(TileContainer, player)
        number_of_tiles: int = tile_container.get_number_of_tiles_of_type(TileTypeEnum.oreMineDeepTunnelTwin)
        return number_of_tiles * 2


class OreMiningTwoCard(BaseOreMiningCard):
    def __init__(self):
        BaseOreMiningCard.__init__(self, card_ids.OreMiningTwoCardId)

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        amount_of_ore: int = 1 if self.has_resources else 2
        self.give_resource(ResourceTypeEnum.ore, amount_of_ore)

        return self.resources


class OreMiningThreeCard(BaseOreMiningCard):
    def __init__(self) -> None:
        BaseOreMiningCard.__init__(self, card_ids.OreMiningThreeCardId)

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        amount_of_ore: int = 2 if self.has_resources else 3
        self.give_resource(ResourceTypeEnum.ore, amount_of_ore)

        return self.resources
