from typing import Dict, List, Union, Tuple, Optional

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from core.services.base_player_service import BasePlayerService
from common.entities.result_lookup import ResultLookup
from common.entities.weapon import Weapon
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum, TileDirectionEnum

# TODO: Update this
from core.enums.harvest_type_enum import HarvestTypeEnum


class MockPlayer(BasePlayerService):
    def __init__(
            self,
            player_id: int,
            tiles: List[BaseTile] = None,
            resources: Dict[ResourceTypeEnum, int] = None):
        BasePlayerService.__init__(self, player_id, 0)
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

    def get_player_choice_use_dwarf_out_of_order(
            self,
            dwarves: List[Dwarf],
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[bool]:
        pass

    def get_player_choice_dwarf_to_use_out_of_order(
            self, dwarves: List[Dwarf],
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[Dwarf]:
        pass

    def get_player_choice_card_to_use(
            self,
            available_cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> \
            ResultLookup[BaseCard]:
        pass

    def get_player_choice_actions_to_use(
            self,
            available_action_choices: List[ActionChoiceLookup],
            turn_index: int, round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[ActionChoiceLookup]:
        pass

    def get_player_choice_expedition_reward(
            self,
            possible_expedition_rewards: List[BaseAction],
            expedition_level: int,
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[List[BaseAction]]:
        pass

    def get_player_choice_tile_to_build(
            self,
            possible_tiles: List[BaseTile],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[BaseTile]:
        pass

    def get_player_choice_location_to_build(
            self,
            tile: BaseTile,
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[Tuple[int, Optional[TileDirectionEnum]]]:
        pass
