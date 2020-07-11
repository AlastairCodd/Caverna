from typing import Union, List, Dict, Callable

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from common.entities.weapon import Weapon
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum


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

        self._use_dwarf_out_of_order_func: Callable[
            [List[Dwarf],
             List[BaseCard],
             int,
             int,
             HarvestTypeEnum],
            ResultLookup[bool]] \
            = lambda info_dwarves, info_cards, info_turn_index, info_round_index, info_harvest_type: ResultLookup(errors="Not Implemented")
        self._dwarf_to_use_out_of_order_func: Callable[
            [List[Dwarf],
             List[BaseCard],
             int,
             int,
             HarvestTypeEnum],
            ResultLookup[Dwarf]] \
            = lambda info_dwarves, info_cards, info_turn_index, info_round_index, info_harvest_type: ResultLookup(errors="Not Implemented")
        self._action_choice_to_use_func: Callable[
            [List[ActionChoiceLookup],
             int,
             int,
             HarvestTypeEnum],
            ResultLookup[ActionChoiceLookup]] \
            = lambda info_possible_action_choices, info_turn_index, info_round_index, info_harvest_type: ResultLookup(errors="Not Implemented")
        self._card_choice_to_use_func: Callable[
            [List[BaseCard],
             int,
             int,
             HarvestTypeEnum],
            ResultLookup[BaseCard]] \
            = lambda info_available_cards, info_turn_index, info_round_index, info_harvest_type: ResultLookup(errors="Not Implemented")

    def get_player_choice_use_dwarf_out_of_order_returns(
            self,
            func: Callable[
                [List[Dwarf],
                 List[BaseCard],
                 int,
                 int,
                 HarvestTypeEnum],
                ResultLookup[bool]]) -> None:
        self._use_dwarf_out_of_order_func = func

    def get_player_choice_use_dwarf_out_of_order(
            self,
            dwarves: List[Dwarf],
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) \
            -> ResultLookup[Dwarf]:
        return self._use_dwarf_out_of_order_func(dwarves, cards, turn_index, round_index, harvest_type)

    def get_player_choice_dwarf_to_use_out_of_order_returns(
            self,
            func: Callable[
                [List[Dwarf],
                 List[BaseCard],
                 int,
                 int,
                 HarvestTypeEnum],
                ResultLookup[Dwarf]]) -> None:
        self._dwarf_to_use_out_of_order_func = func

    def get_player_choice_actions_to_use_returns(
            self,
            func: Callable[
                [List[ActionChoiceLookup],
                 int,
                 int,
                 HarvestTypeEnum],
                ResultLookup[ActionChoiceLookup]]) -> None:
        self._action_choice_to_use_func = func

    def get_player_choice_card_to_use_returns(
            self,
            func: Callable[
                [List[BaseCard],
                 int,
                 int,
                 HarvestTypeEnum],
                ResultLookup[BaseCard]]) -> None:
        self._card_choice_to_use_func = func

    def get_player_choice_dwarf_to_use_out_of_order(
            self,
            dwarves: List[Dwarf],
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[Dwarf]:
        return self._dwarf_to_use_out_of_order_func(
            dwarves,
            cards,
            turn_index,
            round_index,
            harvest_type)

    def get_player_choice_discount(
            self,
            possible_prices: List[Dict[ResourceTypeEnum, int]],
            target: Union[BaseTile, Weapon]) -> Dict[ResourceTypeEnum, int]:
        pass

    def get_player_choice_breed_animals(
            self,
            animals_which_can_reproduce: List[ResourceTypeEnum],
            possible_number_of_animals_to_reproduce: int) -> List[ResourceTypeEnum]:
        pass

    def get_player_choice_market_action(
            self,
            possible_items_and_costs: Dict[ResourceTypeEnum, int]) -> List[ResourceTypeEnum]:
        pass

    def get_player_choice_card_to_use(
            self,
            available_cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[BaseCard]:
        pass

    def get_player_choice_weapon_level(self) -> int:
        pass

    def get_player_choice_actions_to_use(
            self,
            available_action_choices: List[ActionChoiceLookup],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[ActionChoiceLookup]:
        return self._action_choice_to_use_func(
            available_action_choices,
            turn_index,
            round_index,
            harvest_type)

    def get_player_choice_expedition_reward(
            self,
            possible_expedition_rewards: List[BaseAction],
            expedition_level: int,
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[List[BaseAction]]:
        pass
