from typing import List, Dict, Tuple, Optional, Callable

from buisness_logic.effects.base_effects import BaseOnPurchaseEffect
from buisness_logic.effects.purchase_effects import BaseTilePurchaseEffect
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
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
            override_cost: Optional[Dict[ResourceTypeEnum, int]] = None):
        self._tile_type: TileTypeEnum = tile_type
        self._specific_tile_generation_method: Optional[Callable[[], BaseTile]] = specific_tile_generation_method
        if specific_tile_generation_method is None and override_cost is not None:
            raise ValueError("Cannot override cost of unknown specific tile.")
        self._tile_cost_override: Optional[Dict[ResourceTypeEnum, int]] = override_cost

        self._tile_service: TileService = TileService()

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

        if self._specific_tile_generation_method is None:
            does_tile_have_unique_type: bool = self._tile_service.does_tile_type_have_unique_tile(self._tile_type)

            if does_tile_have_unique_type:
                self._specific_tile_generation_method = self._tile_service.get_unique_tile_generation_method(self._tile_type)
            else:
                possible_tiles: List[BaseTile] = self._tile_service.get_possible_tiles(turn_descriptor.tiles, self._tile_type)
                specific_tile_to_build_result: ResultLookup[BaseTile] = player.get_player_choice_tile_to_build(
                    possible_tiles,
                    turn_descriptor)

                success = specific_tile_to_build_result.flag
                errors.extend(specific_tile_to_build_result.errors)

                if specific_tile_to_build_result.flag:
                    # That this returns the same instance as in turn_descriptor.tiles is not an issue, since that item will be removed when it is placed
                    self._specific_tile_generation_method = lambda: specific_tile_to_build_result.value

        if success:
            # TODO: Make this value a type
            location_to_build_result: ResultLookup[Tuple[int, TileDirectionEnum]] = player.get_player_choice_location_to_build(
                self._specific_tile_generation_method(),
                turn_descriptor)

            success = location_to_build_result.flag
            errors.extend(location_to_build_result.errors)

            if location_to_build_result.flag:
                self._tile_location = location_to_build_result.value[0]
                self._tile_direction = location_to_build_result.value[1]

        if success:
            self._effects_to_use: Dict[BaseTilePurchaseEffect, int] = player.get_player_choice_effects_to_use_for_cost_discount(
                self._specific_tile_generation_method(),
                turn_descriptor)

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
        if self._specific_tile_generation_method is None:
            raise ValueError("Must choose a tile to place")

        specific_tile: BaseTile = self._specific_tile_generation_method()
        is_tile_available: bool = self._tile_service.is_tile_available(specific_tile)
        can_place_tile_at_chosen_location: bool = self._tile_service.can_place_tile_at_location(
            player,
            specific_tile,
            self._tile_location,
            self._tile_direction)

        errors: List[str] = []

        has_effects_result: ResultLookup[bool] = self.does_player_have_effects(player)

        errors.extend(has_effects_result.errors)

        if not is_tile_available:
            errors.append("Tile has already been built")

        actual_cost_of_tile_result: ResultLookup[Dict[ResourceTypeEnum, int]] = self._tile_service.get_cost_of_tile(
            specific_tile,
            self._effects_to_use,
            self._tile_cost_override)
        errors.extend(actual_cost_of_tile_result.errors)

        if actual_cost_of_tile_result.flag:
            can_player_afford_tile: bool = player.has_more_resources_than(actual_cost_of_tile_result.value)
            if not can_player_afford_tile:
                errors.append(f"Player cannot afford tile (cost: {actual_cost_of_tile_result.value}, player resources: {player.resources})")

        if not can_place_tile_at_chosen_location:
            errors.append(f"Chosen location {self._tile_location} is invalid")

        success: bool = len(errors) == 0

        if success:
            was_tile_placed_successfully_result: ResultLookup[bool] = self._tile_service.place_tile(
                player,
                specific_tile,
                self._tile_location,
                self._tile_direction)

            success = was_tile_placed_successfully_result.flag
            errors.extend(was_tile_placed_successfully_result.errors)

            if success:
                player.take_resources(actual_cost_of_tile_result.value)

                for effect in specific_tile.effects:
                    if isinstance(effect, BaseOnPurchaseEffect):
                        success &= effect.invoke(player)

        result: ResultLookup[int] = ResultLookup(success, 1 if success else 0, errors)
        return result

    def does_player_have_effects(
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
                warning: str = f"Player wanted to use effect {effect} {number_of_times_wants_to_use} times, can only use {number_of_times_cant_use}"
                errors.append(warning)

        success: bool = len(errors) == 0
        return ResultLookup(success, success, errors)

    def new_turn_reset(self) -> None:
        self._tile_location = -1
        self._tile_direction = None
        self._effects_to_use = {}
