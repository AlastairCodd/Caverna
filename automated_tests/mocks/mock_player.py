from typing import Union, List, Dict, Callable, Tuple, Optional

from buisness_logic.effects.purchase_effects import BaseTilePurchaseEffect
from common.defaults.tile_container_default import TileContainerDefault
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.services.base_player_service import BasePlayerService
from common.entities.result_lookup import ResultLookup
from common.entities.weapon import Weapon
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum, TileDirectionEnum


class MockPlayer(BasePlayerService):
    def __init__(
            self,
            dwarves: Union[List[Dwarf], None] = None,
            resources: Union[Dict[ResourceTypeEnum, int], None] = None,
            player_id: int = 1,
            turn_index: int = 2):
        BasePlayerService.__init__(self, player_id, turn_index, TileContainerDefault())

        if dwarves is not None:
            self._dwarves = dwarves
        if resources is not None:
            self._resources = resources

        self._use_dwarf_out_of_order_func: Callable[
            [List[Dwarf],
             TurnDescriptorLookup],
            ResultLookup[bool]] \
            = lambda info_dwarves, info_turn_descriptor: ResultLookup(errors="Not Implemented")
        self._dwarf_to_use_out_of_order_func: Callable[
            [List[Dwarf],
             TurnDescriptorLookup],
            ResultLookup[Dwarf]] \
            = lambda info_dwarves, info_turn_descriptor: ResultLookup(errors="Not Implemented")
        self._action_choice_to_use_func: Callable[
            [List[ActionChoiceLookup],
             TurnDescriptorLookup],
            ResultLookup[ActionChoiceLookup]] \
            = lambda info_possible_action_choices, info_turn_descriptor: ResultLookup(errors="Not Implemented")
        self._card_choice_to_use_func: Callable[
            [List[BaseCard],
             TurnDescriptorLookup],
            ResultLookup[BaseCard]] \
            = lambda info_available_cards, info_turn_descriptor: ResultLookup(errors="Not Implemented")
        self._location_to_build_func: Callable[
            [BaseTile,
             TurnDescriptorLookup,
             Optional[BaseTile]],
            ResultLookup[Tuple[int, Optional[TileDirectionEnum]]]] \
            = lambda info_tile, info_turn_descriptor, info_secondary_tile: ResultLookup(errors="Not Implemented")
        self._tile_to_build_func: Callable[
            [List[BaseTile],
             TurnDescriptorLookup],
            ResultLookup[BaseTile]] \
            = lambda info_tiles, info_turn_descriptor: ResultLookup(errors="Not Implemented")
        self._effects_to_use_for_cost_discount: Callable[
            [BaseTile,
             TurnDescriptorLookup,
             Optional[BaseTile]],
            Dict[BaseTilePurchaseEffect, int]] \
            = lambda info_tile, info_turn_descriptor, info_secondary_tile: {}

    def get_player_choice_use_dwarf_out_of_order_returns(
            self,
            func: Callable[
                [List[Dwarf],
                 TurnDescriptorLookup],
                ResultLookup[bool]]) -> None:
        self._use_dwarf_out_of_order_func = func

    def get_player_choice_use_dwarf_out_of_order(
            self,
            dwarves: List[Dwarf],
            turn_descriptor: TurnDescriptorLookup) \
            -> ResultLookup[Dwarf]:
        return self._use_dwarf_out_of_order_func(dwarves, turn_descriptor)

    def get_player_choice_dwarf_to_use_out_of_order_returns(
            self,
            func: Callable[
                [List[Dwarf],
                 TurnDescriptorLookup],
                ResultLookup[Dwarf]]) -> None:
        self._dwarf_to_use_out_of_order_func = func

    def get_player_choice_actions_to_use_returns(
            self,
            func: Callable[
                [List[ActionChoiceLookup],
                 TurnDescriptorLookup],
                ResultLookup[ActionChoiceLookup]]) -> None:
        self._action_choice_to_use_func = func

    def get_player_choice_card_to_use_returns(
            self,
            func: Callable[
                [List[BaseCard],
                 TurnDescriptorLookup],
                ResultLookup[BaseCard]]) -> None:
        self._card_choice_to_use_func = func

    def get_player_choice_location_to_build_returns(
            self,
            func: Callable[
                [BaseTile,
                 TurnDescriptorLookup,
                 Optional[BaseTile]],
                ResultLookup[Tuple[int, Optional[TileDirectionEnum]]]]) -> None:
        self._location_to_build_func = func

    def get_player_choice_tile_to_build_returns(
            self,
            func: Callable[
                [List[BaseTile],
                 TurnDescriptorLookup],
                ResultLookup[BaseTile]]) -> None:
        self._tile_to_build_func = func

    def get_player_choice_effects_to_use_for_cost_discount_returns(
            self,
            func: Callable[
                [BaseTile,
                 TurnDescriptorLookup,
                 Optional[BaseTile]],
                Dict[BaseTilePurchaseEffect, int]]) -> None:
        self._effects_to_use_for_cost_discount = func

    def get_player_choice_dwarf_to_use_out_of_order(
            self,
            dwarves: List[Dwarf],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[Dwarf]:
        return self._dwarf_to_use_out_of_order_func(dwarves, turn_descriptor)

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
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[BaseCard]:
        return self._card_choice_to_use_func(available_cards, turn_descriptor)

    def get_player_choice_weapon_level(self) -> int:
        pass

    def get_player_choice_actions_to_use(
            self,
            available_action_choices: List[ActionChoiceLookup],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        return self._action_choice_to_use_func(available_action_choices, turn_descriptor)

    def get_player_choice_expedition_reward(
            self,
            possible_expedition_rewards: List[BaseAction],
            expedition_level: int,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[List[BaseAction]]:
        pass

    def get_player_choice_tile_to_build(
            self,
            possible_tiles: List[BaseTile],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[BaseTile]:
        return self._tile_to_build_func(possible_tiles, turn_descriptor)

    def get_player_choice_location_to_build(
            self,
            tile: BaseTile,
            turn_descriptor: TurnDescriptorLookup,
            secondary_tile: Optional[BaseTile] = None) -> ResultLookup[Tuple[int, Optional[TileDirectionEnum]]]:
        return self._location_to_build_func(tile, turn_descriptor, secondary_tile)

    def get_player_choice_effects_to_use_for_cost_discount(
            self,
            specific_tile: BaseTile,
            turn_descriptor: TurnDescriptorLookup,
            secondary_tile: Optional[BaseTile] = None) -> Dict[BaseTilePurchaseEffect, int]:
        return self._effects_to_use_for_cost_discount(specific_tile, turn_descriptor, secondary_tile)
