from typing import Dict, cast

from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import ResourceTypeEnum, ActionCombinationEnum, TileTypeEnum
from core.containers.resource_container import ResourceContainer
from buisness_logic.actions import *
from core.repositories.base_player_repository import BasePlayerRepository


class RubyMiningCard(BaseCard, ResourceContainer):

    def __init__(self):
        BaseCard.__init__(
            self, "Ruby Mining", 33, 4,
            Conditional(
                ActionCombinationEnum.AndThenOr,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                receive_conditionally_action.ReceiveConditionallyAction(
                    self._condition,
                    {ResourceTypeEnum.ruby: 1})
            ))
        ResourceContainer.__init__(self)

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
