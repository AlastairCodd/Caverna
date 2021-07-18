from typing import Optional, List, Dict

from buisness_logic.actions.cannot_afford_action_error import CannotAffordActionError
from buisness_logic.effects.purchase_effects import BaseTilePurchaseEffect
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.services.tile_service import TileService
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.constants import game_constants
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class PlaceAStableAction(BasePlayerChoiceAction):
    def __init__(
            self,
            override_cost: Optional[Dict[ResourceTypeEnum, int]] = None):
        self._tile_service: TileService = TileService()

        self._stable_cost: Optional[Dict[ResourceTypeEnum, int]] = {ResourceTypeEnum.stone: 1} if override_cost is None else override_cost

        self._tile_location: int = -1
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

        if success:
            location_to_build_result: ResultLookup[int] = player.get_player_choice_location_to_build_stable(turn_descriptor)

            success = location_to_build_result.flag
            errors.extend(location_to_build_result.errors)

            if location_to_build_result.flag:
                self._tile_location = location_to_build_result.value

        if success:
            possible_purchase_effects: List[BaseTilePurchaseEffect] = self._tile_service.get_purchase_effects(player, turn_descriptor.tiles)

            self._effects_to_use = player.get_player_choice_effects_to_use_for_cost_discount(
                self._stable_cost,
                possible_purchase_effects,
                turn_descriptor)

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
        if self._tile_location == -1:
            raise ValueError("Player choice has not been made")
        if self._tile_location < 0 or self._tile_location > player.tile_count:
            raise IndexError(f"Tile must be placed within bounds (0<={self._tile_location}<={player.tile_count})")

        result: ResultLookup[int]
        errors: List[str] = []

        has_effects_result: ResultLookup[bool] = self._does_player_have_effects(player)
        errors.extend(has_effects_result.errors)

        does_player_have_stable_to_place: bool = self._does_player_have_stable_to_place(player)
        if not does_player_have_stable_to_place:
            errors.append("Player has already placed all stables")

        can_place_stable_at_chosen_location: bool = not player.get_tile_at_location(self._tile_location).has_stable

        if not can_place_stable_at_chosen_location:
            errors.append(f"Chosen location {self._tile_location} already has a stable")

        actual_cost_of_stable_result: ResultLookup[Dict[ResourceTypeEnum, int]] = self._tile_service.get_cost_of_tile(
            None,
            self._stable_cost,
            self._effects_to_use)
        errors.extend(actual_cost_of_stable_result.errors)

        if actual_cost_of_stable_result.flag:
            can_player_afford_stable: bool = player.has_more_resources_than(actual_cost_of_stable_result.value)
            if not can_player_afford_stable:
                errors.append(CannotAffordActionError("Player", "stable", actual_cost_of_stable_result.value, player.resources))

        success: bool = len(errors) == 0

        if success:
            was_tile_placed_successfully_result: bool = player.get_tile_at_location(self._tile_location).give_stable()

            success = was_tile_placed_successfully_result

            if success:
                success = player.take_resources(actual_cost_of_tile_result.value)

        result: ResultLookup[int] = ResultLookup(success, 1 if success else 0, errors)
        return result

    def new_turn_reset(self) -> None:
        self._tile_location = -1
        self._effects_to_use = {}
        self._turn_descriptor = None

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

    def _does_player_have_stable_to_place(
            self,
            player: BasePlayerRepository) -> bool:
        if player is None:
            raise ValueError("Player cannot be None")
        number_of_stables_remaining: int = game_constants.maximum_number_of_stables
        for tile in player.tiles.values():
            if tile.has_stable:
                number_of_stables_remaining -= 1
            if number_of_stables_remaining == 0:
                break
        result: bool = number_of_stables_remaining > 0
        return result

    def __str__(self) -> str:
        if self._stable_cost is None or not any(self._stable_cost):
            return "Place a stable (for free)"
        result: str = "Place a stable for " + " and ".join([f"{amount} {resource.name}" for resource, amount in self._stable_cost.items()])
        return result
