from typing import Dict

from buisness_logic.actions import receive_conditionally_action, take_accumulated_items_action
from common.entities.multiconditional import Conditional
from core.baseClasses.base_resource_containing_card import BaseResourceContainingCard
from core.constants import card_ids
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import ActionCombinationEnum, ResourceTypeEnum, TileTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class OreDeliveryCard(BaseResourceContainingCard):
    def __init__(self):
        BaseResourceContainingCard.__init__(
            self, "Ore Delivery", card_ids.OreDeliveryCardId, 3,
            Conditional(
                ActionCombinationEnum.AndThen,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                receive_conditionally_action.ReceiveConditionallyAction(self._condition, {ResourceTypeEnum.ore: 2})
        ))

    def refill_action(self) -> Dict[ResourceTypeEnum, int]:
        self.give_resources(
            {ResourceTypeEnum.stone: 1,
             ResourceTypeEnum.ore: 1})

        return self.resources

    def _condition(self, player: BasePlayerRepository) -> int:
        if player is None:
            raise ValueError(str(player))
        tile_container = cast(TileContainer, player)
        number_of_ore_mines: int = tile_container.get_number_of_tiles_of_type(TileTypeEnum.oreMine)
        return number_of_ore_mines
