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


class PlaceATwinTileAction(BasePlayerChoiceAction):
    def __init__(
            self,
            tile_type: TileTypeEnum,
            override_cost: Optional[Dict[ResourceTypeEnum, int]] = None):
        self._tile_service: TileService = TileService()

        self._tile_type: TileTypeEnum = tile_type
        self._tile_is_twin: bool = self._tile_service.is_tile_a_twin_tile(self._tile_type)

        self._primary_twin_tile_generation_method: Optional[Callable[[], BaseTile]] = None
        self._secondary_twin_tile_generation_method: Optional[Callable[[], BaseTile]] = None

        self._tile_cost_override: Optional[Dict[ResourceTypeEnum, int]] = override_cost

        self._tile_location: int = -1
        self._tile_direction: Optional[TileDirectionEnum] = None
        self._effects_to_use: Dict[BaseTilePurchaseEffect, int] = {}
        self._turn_descriptor: Optional[TurnDescriptorLookup] = None

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("player cannot be none")

        success: bool = True
        errors: List[str] = []

        self._primary_twin_tile_generation_method, self._secondary_twin_tile_generation_method = self._tile_service\
            .get_twin_tile_generation_methods(self._tile_type)

        primary_tile: BaseTile = self._primary_twin_tile_generation_method()
        secondary_tile: BaseTile = self._secondary_twin_tile_generation_method()

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

                if True:
                    if location_to_build_result.value[1] is None:
                        success = False
                        errors.append("Must have direction when placing twin tile")
                    else:
                        self._tile_direction = location_to_build_result.value[1]

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

        if success:
            self._turn_descriptor = turn_descriptor

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
        if self._tile_location == -1 or self._turn_descriptor is None:
            raise ValueError("Player choice has not been made")
        if self._tile_location < 0 or self._tile_location > player.tile_count:
            raise IndexError(f"Tile must be placed within bounds (0<={self._tile_location}<={player.tile_count})")

        if self._primary_twin_tile_generation_method is None:
            raise ValueError("Must choose a tile to place (_primary_twin_tile_generation_method)")
        if self._secondary_twin_tile_generation_method is None:
            raise ValueError("Must choose a tile to place (_secondary_twin_tile_generation_method)")

        errors: List[str] = []

        has_effects_result: ResultLookup[bool] = self._does_player_have_effects(player)

        errors.extend(has_effects_result.errors)

        primary_tile: BaseTile = self._primary_twin_tile_generation_method()
        secondary_tile: BaseTile = self._secondary_twin_tile_generation_method()
        is_twin_tile_inseparable: bool = primary_tile is secondary_tile

        can_place_tiles_at_chosen_location: bool = self._tile_service.can_place_twin_tile_at_location(
            player,
            self._tile_type,
            self._tile_location,
            self._tile_direction)

        if not can_place_tiles_at_chosen_location:
            errors.append(f"Chosen location {self._tile_location} and direction {self._tile_direction} is invalid")

        is_primary_tile_available: bool = self._tile_service.is_tile_available(self._turn_descriptor, primary_tile)
        is_secondary_tile_available: bool = self._tile_service.is_tile_available(self._turn_descriptor, primary_tile)

        if not is_primary_tile_available:
            errors.append(f"Primary Tile in Twin Tile ({primary_tile.name}) has already been built")
        if not is_secondary_tile_available:
            errors.append(f"Secondary Tile in Twin Tile ({secondary_tile.name}) has already been built")

        cost: Dict[ResourceTypeEnum, int] = {}
        was_cost_calculated_successfully: bool = False

        if self._tile_cost_override is None:
            actual_cost_of_primary_tile_result: ResultLookup[Dict[ResourceTypeEnum, int]] = self._tile_service.get_cost_of_tile(
                primary_tile,
                self._tile_cost_override,
                self._effects_to_use)
            errors.extend(actual_cost_of_primary_tile_result.errors)

            actual_cost_of_secondary_tile_result: ResultLookup[Dict[ResourceTypeEnum, int]]
            if not is_twin_tile_inseparable:
                actual_cost_of_secondary_tile_result = self._tile_service.get_cost_of_tile(
                    secondary_tile,
                    self._tile_cost_override,
                    self._effects_to_use)
            else:
                actual_cost_of_secondary_tile_result = ResultLookup(True, {})
            errors.extend(actual_cost_of_secondary_tile_result.errors)

            if actual_cost_of_primary_tile_result.flag and actual_cost_of_secondary_tile_result.flag:
                was_cost_calculated_successfully = True
                cost = {}
                for resource in actual_cost_of_primary_tile_result.value:
                    cost.setdefault(resource, 0)
                    cost[resource] += actual_cost_of_primary_tile_result.value[resource]
                for resource in actual_cost_of_secondary_tile_result.value:
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
                self._tile_type,
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
                if not is_twin_tile_inseparable:
                    for effect in secondary_tile.effects:
                        if isinstance(effect, BaseOnPurchaseEffect):
                            success &= effect.invoke(player)

        result: ResultLookup[int] = ResultLookup(success, 2 if success else 0, errors)
        return result

    def new_turn_reset(self) -> None:
        self._tile_location = -1
        self._tile_direction = None
        self._effects_to_use = {}
        self._turn_descriptor = None

    def _should_get_effects_to_use_on_cost(
            self,
            primary_tile: BaseTile,
            secondary_tile: BaseTile) -> bool:

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
        errors: List[str] = []

        if len(self._effects_to_use) > 0:
            effects_player_has: List[BaseTilePurchaseEffect] = player.get_effects_of_type(BaseTilePurchaseEffect)

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