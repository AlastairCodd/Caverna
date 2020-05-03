from typing import Union, List, Dict

from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from common.entities.weapon import Weapon
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum


class MockPlayer(Player):
    def __init__(
            self,
            dwarves: Union[List[Dwarf], None] = None,
            resources: Union[Dict[ResourceTypeEnum, int], None] = None,
            player_id: int = 1,
            turn_index: int = 2):
        Player.__init__(self, player_id, turn_index)

        if dwarves is not None:
            self._dwarves = dwarves
        if resources is not None:
            self._resources = resources

    def get_player_choice_use_dwarf_out_of_order(self, dwarves: List[Dwarf], resources: Dict[ResourceTypeEnum, int]) \
            -> ResultLookup[Dwarf]:
        return ResultLookup(True, self._dwarves[2])

    def get_player_choice_discount(self, possible_prices: List[Dict[ResourceTypeEnum, int]], target: Union[BaseTile, Weapon]) \
            -> Dict[ResourceTypeEnum, int]:
        pass

    def get_player_choice_breed_animals(self, animals_which_can_reproduce: List[ResourceTypeEnum], possible_number_of_animals_to_reproduce: int) \
            -> List[ResourceTypeEnum]:
        pass

    def get_player_choice_weapon_level(self) \
            -> int:
        pass

    def get_player_choice_market_action(self, possible_items_and_costs: Dict[ResourceTypeEnum, int]) \
            -> List[ResourceTypeEnum]:
        pass