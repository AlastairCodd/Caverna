from typing import List, Dict

from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import ResourceTypeEnum


class BuyFromMarketAction(BaseAction):
    def __init__(self):
        self._possible_items_and_costs: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.dog: 2,
            ResourceTypeEnum.sheep: 1,
            ResourceTypeEnum.donkey: 1,
            ResourceTypeEnum.boar: 1,
            ResourceTypeEnum.cow: 1,
            ResourceTypeEnum.wood: 1,
            ResourceTypeEnum.stone: 1,
            ResourceTypeEnum.ore: 1,
            ResourceTypeEnum.grain: 1,
            ResourceTypeEnum.veg: 1,
        }

    def invoke(self, player: Player, active_card: BaseCard, current_dwarf: Dwarf) -> ResultLookup[int]:
        """Asks the player which things they would like to buy from the market.

        :param player: The player who will buy things. This may not be null.
        :param active_card: Unused.
        :param current_dwarf: Unused.
        :return: True if player chosen items were successfully purchased, false if not.
        """
        if player is None:
            raise ValueError(str(player))

        resources_chosen_by_player: List[ResourceTypeEnum] = player\
            .get_player_choice_market_action(self._possible_items_and_costs)

        total_cost_of_resources_chosen_by_player: int = \
            sum(map(lambda resource: self._possible_items_and_costs[resource], resources_chosen_by_player))

        raise NotImplementedError()

    def new_turn_reset(self):
        pass
