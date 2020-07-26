from typing import Dict, List, Union

from common.entities.player import Player
from common.entities.tile_entity import TileEntity
from common.entities.weapon import Weapon
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum


# TODO: Update this
class MockPlayer(Player):
    def __init__(
            self,
            player_id: int,
            tiles: List[BaseTile] = None,
            resources: Dict[ResourceTypeEnum, int] = None):
        Player.__init__(self, player_id, 0)
        if tiles is None:
            tiles = []
        self._mock_tiles = tiles
        if resources is not None:
            self._resources = resources

    def get_player_choice(self, action):
        pass

    def get_player_choice_market_action(
            self,
            possible_items_and_costs: Dict[ResourceTypeEnum, int]) \
            -> List[ResourceTypeEnum]:
        pass

    def get_player_choice_weapon_level(self) -> int:
        pass

    def get_player_choice_breed_animals(
            self,
            animals_which_can_reproduce: List[ResourceTypeEnum],
            possible_number_of_animals_to_reproduce: int) \
            -> List[ResourceTypeEnum]:
        pass

    def get_player_choice_discount(
            self,
            possible_prices: List[Dict[ResourceTypeEnum, int]],
            target: Union[BaseTile, Weapon]) \
            -> Dict[ResourceTypeEnum, int]:
        pass
