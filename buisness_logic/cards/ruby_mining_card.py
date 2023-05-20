from typing import Dict, cast

from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.constants import card_ids
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class RubyMiningCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Ruby Mining", card_ids.RubyMiningCardId,
            actions=Conditional(
                ActionCombinationEnum.AndThen,
                take_accumulated_items_action.TakeAccumulatedItemsAction(False),
                receive_conditionally_action.ReceiveConditionallyAction(
                    self._condition,
                    {ResourceTypeEnum.ruby: 1},
                    "if you have at least one ruby mine")
            ))

    def _condition(self, player: BasePlayerRepository) -> int:
        if player is None:
            raise ValueError(str(player))
        tile_container: TileContainer = cast(TileContainer, player)
        number_of_tiles: int = tile_container.get_number_of_tiles_of_type(TileTypeEnum.rubyMine)
        result: int = 1 if number_of_tiles > 1 else 0
        return result

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        newResources = {ResourceTypeEnum.ruby: 1} if self.has_resources else {ResourceTypeEnum.ruby: 2}
        self.give_resources(newResources)

        return self.resources
