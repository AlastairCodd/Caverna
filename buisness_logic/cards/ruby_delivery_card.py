from buisness_logic.actions import *
from common.entities.multiconditional import Conditional
from core.baseClasses.base_card import BaseCard
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import ActionCombinationEnum, ResourceTypeEnum, TileTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class RubyDeliveryCard(BaseCard, ResourceContainer):
    def __init__(self):
        BaseCard.__init__(
            self, "Ruby Delivery", 33, 4,
            Conditional(
                ActionCombinationEnum.AndThen,
                take_accumulated_items_action.TakeAccumulatedItemsAction(),
                receive_conditionally_action.ReceiveConditionallyAction(
                    self._condition,
                    {ResourceTypeEnum.ruby: 1})
            ))
        ResourceContainer.__init__(self)

    def _condition(self, player: BasePlayerRepository) -> int:
        if player is None:
            raise ValueError(str(player))
        number_of_tiles: int = player.get_number_of_tiles_of_type(TileTypeEnum.rubyMine)
        result: int = 1 if number_of_tiles > 1 else 0
        return result

