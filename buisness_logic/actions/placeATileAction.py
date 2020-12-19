from typing import List, Dict, Optional, Callable

from buisness_logic.effects.base_effects import BaseOnPurchaseEffect
from buisness_logic.effects.purchase_effects import BaseTilePurchaseEffect
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.tile_unknown_placement_lookup import TileUnknownPlacementLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.services.tile_service import TileService
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum, TileDirectionEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class PlaceATileAction(BasePlayerChoiceAction):
    def __init__(
            self,
            tile_type: TileTypeEnum,
            specific_tile_generation_method: Optional[Callable[[], BaseTile]] = None,
            override_cost: Optional[Dict[ResourceTypeEnum, int]] = None,
            override_requisite: Optional[List[TileTypeEnum]] = None):
        self._tile_service: TileService = TileService()

        self._tile_type: TileTypeEnum = tile_type
        self._tile_is_twin: bool = self._tile_service.is_tile_a_twin_tile(self._tile_type)

        # if tile is not twin, _specific_tile_generation_method should be referenced
        self._specific_tile_generation_method: Optional[Callable[[], BaseTile]]
        # otherwise the _primary/secondary_twin_tile_generation methods will be populated
        self._primary_twin_tile_generation_method: Optional[Callable[[], BaseTile]] = None
        self._secondary_twin_tile_generation_method: Optional[Callable[[], BaseTile]] = None

        if self._tile_is_twin:
            if specific_tile_generation_method is not None:
                raise ValueError("Specific tile is not valid for twin tiles.")
            self._specific_tile_generation_method = None

            if override_requisite is not None:
                raise ValueError("Cannot override requisites for twin tiles.")
        else:
            if specific_tile_generation_method is None and override_cost is not None:
                raise ValueError("Cannot override cost of unknown specific tile.")
            self._specific_tile_generation_method = specific_tile_generation_method

            self._tile_requisites_override: Optional[List[TileTypeEnum]] = override_requisite
        self._tile_cost_override: Optional[Dict[ResourceTypeEnum, int]] = override_cost

        self._tile_location: int = -1
        self._tile_direction: Optional[TileDirectionEnum] = None
        self._effects_to_use: Dict[BaseTilePurchaseEffect, int] = {}

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("player cannot be none")

        success: bool = True
        errors: List[str] = []

        if self._tile_is_twin:
            self._primary_twin_tile_generation_method, self._secondary_twin_tile_generation_method \
                = self._tile_service.get_twin_tile_generation_methods(self._tile_type)
        else:
            if self._specific_tile_generation_method is None:
                does_tile_have_unique_type: bool = self._tile_service.does_tile_type_have_unique_tile(self._tile_type)

                if does_tile_have_unique_type:
                    self._specific_tile_generation_method = self._tile_service \
                        .get_unique_tile_generation_method(self._tile_type)
                else:
                    possible_tiles: List[BaseTile] = self._tile_service \
                        .get_possible_tiles(turn_descriptor.tiles, self._tile_type)
                    specific_tile_to_build_result: ResultLookup[BaseTile] = player.get_player_choice_tile_to_build(
                        possible_tiles,
                        turn_descriptor)

                    success = specific_tile_to_build_result.flag
                    errors.extend(specific_tile_to_build_result.errors)

                    if specific_tile_to_build_result.flag:
                        # That this returns the same instance as in turn_descriptor.tiles is not an issue,
                        # since that item will be removed when it is placed
                        # TODO: Do what this comment says
                        self._specific_tile_generation_method = lambda: specific_tile_to_build_result.value

        primary_tile: BaseTile
        secondary_tile: Optional[BaseTile]

        if self._tile_is_twin:
            primary_tile = self._primary_twin_tile_generation_method()
            secondary_tile = self._secondary_twin_tile_generation_method()
        else:
            primary_tile = self._specific_tile_generation_method()
            secondary_tile = None

        if success:
            location_to_build_result: ResultLookup[TileUnknownPlacementLookup] = player \
                .get_player_choice_location_to_build(
                primary_tile,
                turn_descriptor,
                secondary_tile)

            success = location_to_build_result.flag
            errors.extend(location_to_build_result.errors)

            if location_to_build_result.flag:
                self._tile_location = location_to_build_result.value[0]

                if self._tile_is_twin:
                    if location_to_build_result.value[1] is None:
                        success = False
                        errors.append("Must have direction when placing twin tile")
                    else:
                        self._tile_direction = location_to_build_result.value[1]
                elif location_to_build_result.value[1] is not None:
                    self._tile_direction = location_to_build_result.value[1]
                    error: str = f"Warning: direction to place tile is meaningless when placing single tile {self._tile_type}"
                    errors.append(error)

        if success:
            should_get_effects_to_use_on_cost: bool = self._should_get_effects_to_use_on_cost(
                primary_tile,
                secondary_tile)

            if should_get_effects_to_use_on_cost:
                self._effects_to_use = player.get_player_choice_effects_to_use_for_cost_discount(
                    primary_tile,
                    turn_descriptor,
                    secondary_tile)
            else:
                self._effects_to_use = {}

        result: ResultLookup[ActionChoiceLookup] = ResultLookup(
            success,
            ActionChoiceLookup([]),
            errors)
        return result

    def invoke(
            self,
            player: BasePlayerRepository,
            active_card: BaseCard,
            current_dwarf: Dwarf) -> ResultLookup[int]:
        if player is None:
            raise ValueError("Player may not be none")
        if self._tile_location < 0 or self._tile_location > player.tile_count:
            raise IndexError(f"Tile must be placed within bounds (0<={self._tile_location}<={player.tile_count})")

        if self._tile_is_twin:
            if self._primary_twin_tile_generation_method is None:
                raise ValueError("Must choose a tile to place (_primary_twin_tile_generation_method)")
            if self._secondary_twin_tile_generation_method is None:
                raise ValueError("Must choose a tile to place (_secondary_twin_tile_generation_method)")
        else:
            if self._specific_tile_generation_method is None:
                raise ValueError("Must choose a tile to place (_specific_tile_generation_method)")

        result: ResultLookup[int]
        errors: List[str] = []

        has_effects_result: ResultLookup[bool] = self._does_player_have_effects(player)

        errors.extend(has_effects_result.errors)

        if self._tile_is_twin:
            result = self.invoke_for_twin_tile(player, errors)
        else:
            result = self.invoke_for_single_tile(player, errors)
        return result

    def new_turn_reset(self) -> None:
        self._tile_location = -1
        self._tile_direction = None
        self._effects_to_use = {}

    def invoke_for_twin_tile(
            self,
            player: BasePlayerRepository,
            errors: List[str]) -> ResultLookup[int]:
        if player is None:
            raise ValueError("Player may not be none")
        if errors is None:
            raise ValueError("Errors may not be none")
        primary_tile: BaseTile = self._primary_twin_tile_generation_method()
        secondary_tile: BaseTile = self._secondary_twin_tile_generation_method()

        can_place_tiles_at_chosen_location: bool = self._tile_service.can_place_twin_tile_at_location(
            player,
            primary_tile,
            secondary_tile,
            self._tile_location,
            self._tile_direction)

        if not can_place_tiles_at_chosen_location:
            errors.append(f"Chosen location {self._tile_location} and direction {self._tile_direction} is invalid")

        is_primary_tile_available: bool = self._tile_service.is_tile_available(primary_tile)
        is_secondary_tile_available: bool = self._tile_service.is_tile_available(primary_tile)

        if not is_primary_tile_available:
            errors.append(f"Primary Tile in Twin Tile ({primary_tile.name}) has already been built")
        if not is_secondary_tile_available:
            errors.append(f"secondary Tile in Twin Tile ({secondary_tile.name}) has already been built")

        cost: Dict[ResourceTypeEnum, int] = {}
        was_cost_calculated_successfully: bool = False

        if self._tile_cost_override is None:
            actual_cost_of_primary_tile_result: ResultLookup[Dict[ResourceTypeEnum, int]] = self._tile_service.get_cost_of_tile(
                primary_tile,
                self._tile_cost_override,
                self._effects_to_use)
            actual_cost_of_secondary_tile_result: ResultLookup[Dict[ResourceTypeEnum, int]] = self._tile_service.get_cost_of_tile(
                secondary_tile,
                self._tile_cost_override,
                self._effects_to_use)
            errors.extend(actual_cost_of_primary_tile_result.errors)
            errors.extend(actual_cost_of_secondary_tile_result.errors)

            if actual_cost_of_primary_tile_result.flag and actual_cost_of_secondary_tile_result.flag:
                was_cost_calculated_successfully = True
                cost = {}
                for resource in actual_cost_of_primary_tile_result.value:
                    cost.setdefault(resource, 0)
                    cost[resource] += actual_cost_of_primary_tile_result.value[resource]
                for resource in actual_cost_of_primary_tile_result.value:
                    cost.setdefault(resource, 0)
                    cost[resource] += actual_cost_of_primary_tile_result.value[resource]
        else:
            overridden_cost_result: ResultLookup[Dict[ResourceTypeEnum, int]] = self._tile_service.get_cost_of_tile(
                cost_override=self._tile_cost_override,
                effects_to_use=self._effects_to_use)

            errors.extend(overridden_cost_result.errors)

            if overridden_cost_result.flag:
                was_cost_calculated_successfully = True
                cost = overridden_cost_result.value

        if was_cost_calculated_successfully:
            can_player_afford_tile: bool = player.has_more_resources_than(cost)
            if not can_player_afford_tile:
                errors.append(f"Player cannot afford tile (\r\ncost: {cost},\r\n" +
                              f"player resources: {player.resources})")

        success: bool = len(errors) == 0
        if success:
            was_tile_placed_successfully_result: ResultLookup[bool] = self._tile_service.place_twin_tile(
                player,
                primary_tile,
                secondary_tile,
                self._tile_location,
                self._tile_direction)

            success = was_tile_placed_successfully_result.flag
            errors.extend(was_tile_placed_successfully_result.errors)

            if success:
                success = player.take_resources(cost)

                for effect in primary_tile.effects:
                    if isinstance(effect, BaseOnPurchaseEffect):
                        success &= effect.invoke(player)
                for effect in secondary_tile.effects:
                    if isinstance(effect, BaseOnPurchaseEffect):
                        success &= effect.invoke(player)

        result: ResultLookup[int] = ResultLookup(success, 2 if success else 0, errors)
        return result

    def invoke_for_single_tile(
            self,
            player: BasePlayerRepository,
            errors: List[str]) -> ResultLookup[int]:
        if player is None:
            raise ValueError("Player may not be none")
        if errors is None:
            raise ValueError("Errors may not be none")
        specific_tile: BaseTile = self._specific_tile_generation_method()
        is_tile_available: bool = self._tile_service.is_tile_available(specific_tile)
        can_place_tile_at_chosen_location: bool = self._tile_service.can_place_tile_at_location(
            player,
            specific_tile,
            self._tile_location,
            self._tile_requisites_override)

        if not is_tile_available:
            errors.append(f"Tile ({specific_tile.name}) has already been built")

        if not can_place_tile_at_chosen_location:
            errors.append(f"Chosen location {self._tile_location} is invalid")

        actual_cost_of_tile_result: ResultLookup[Dict[ResourceTypeEnum, int]] = self._tile_service.get_cost_of_tile(
            specific_tile,
            self._tile_cost_override,
            self._effects_to_use)
        errors.extend(actual_cost_of_tile_result.errors)

        if actual_cost_of_tile_result.flag:
            can_player_afford_tile: bool = player.has_more_resources_than(actual_cost_of_tile_result.value)
            if not can_player_afford_tile:
                errors.append(f"Player cannot afford tile (cost: {actual_cost_of_tile_result.value}," +
                              f" player resources: {player.resources})")

        success: bool = len(errors) == 0

        if success:
            was_tile_placed_successfully_result: ResultLookup[bool] = self._tile_service.place_single_tile(
                player,
                specific_tile,
                self._tile_location,
                self._tile_requisites_override)

            success = was_tile_placed_successfully_result.flag
            errors.extend(was_tile_placed_successfully_result.errors)

            if success:
                success = player.take_resources(actual_cost_of_tile_result.value)

                for effect in specific_tile.effects:
                    if isinstance(effect, BaseOnPurchaseEffect):
                        success &= effect.invoke(player)

        result: ResultLookup[int] = ResultLookup(success, 1 if success else 0, errors)
        return result

    def _should_get_effects_to_use_on_cost(
            self,
            primary_tile: BaseTile,
            secondary_tile: Optional[BaseTile]) -> bool:

        do_tiles_have_cost: bool = self._tile_cost_override is not None

        if not do_tiles_have_cost:
            primary_tile_cost_result: ResultLookup[Dict[ResourceTypeEnum, int]] = self._tile_service \
                .get_cost_of_tile(primary_tile)
            # Since we are not providing any effects, the flag will always be true
            primary_tile_cost: Dict[ResourceTypeEnum, int] = primary_tile_cost_result.value
            do_tiles_have_cost = any(primary_tile_cost[resource] for resource in primary_tile_cost)

        if not do_tiles_have_cost and secondary_tile is not None:
            secondary_tile_cost_result: ResultLookup[Dict[ResourceTypeEnum, int]] = self._tile_service \
                .get_cost_of_tile(secondary_tile)
            # Since we are not providing any effects, the flag will always be true
            secondary_tile_cost: Dict[ResourceTypeEnum, int] = secondary_tile_cost_result.value
            do_tiles_have_cost = any(secondary_tile_cost[resource] for resource in secondary_tile_cost)
        return do_tiles_have_cost

    def _does_player_have_effects(
            self,
            player: BasePlayerRepository) -> ResultLookup[bool]:
        effects_player_has: List[BaseTilePurchaseEffect] = player.get_effects_of_type(BaseTilePurchaseEffect)

        errors: List[str] = []
        effect: BaseTilePurchaseEffect
        for effect in self._effects_to_use:
            number_of_times_wants_to_use: int = self._effects_to_use[effect]
            number_of_times_cant_use: int = number_of_times_wants_to_use

            effect_player_has: BaseTilePurchaseEffect
            for effect_player_has in effects_player_has:
                if effect_player_has == effect:
                    if effect.can_be_used_only_once:
                        number_of_times_cant_use -= 1
                    else:
                        number_of_times_cant_use = 0
            if number_of_times_cant_use > 0:
                warning: str = f"Player wanted to use effect {effect} {number_of_times_wants_to_use} times," \
                               + f" can only use {number_of_times_cant_use}"
                errors.append(warning)

        success: bool = len(errors) == 0
        return ResultLookup(success, success, errors)
