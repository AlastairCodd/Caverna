from typing import List, Dict, Optional, Callable

from buisness_logic.actions.cannot_afford_action_error import CannotAffordActionError
from buisness_logic.actions.receive_action import ReceiveAction
from buisness_logic.effects.base_effects import BaseOnPurchaseEffect
from buisness_logic.effects.purchase_effects import BaseTilePurchaseEffect
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.precedes_constraint import PrecedesConstraint
from common.entities.result_lookup import ResultLookup
from common.services.tile_service import TileService
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class PlaceASingleTileAction(BasePlayerChoiceAction):
    def __init__(
            self,
            tile_type: TileTypeEnum,
            specific_tile_generation_method: Optional[Callable[[], BaseTile]] = None,
            override_cost: Optional[Dict[ResourceTypeEnum, int]] = None,
            override_requisite: Optional[List[TileTypeEnum]] = None):
        self._tile_service: TileService = TileService()

        self._tile_type: TileTypeEnum = tile_type
        tile_is_twin: bool = self._tile_service.is_tile_a_twin_tile(self._tile_type)
        if tile_is_twin:
            raise ValueError(f"Tile type {self._tile_type} cannot be placed a single tile")

        if specific_tile_generation_method is None and \
                not self._tile_service.does_tile_type_have_unique_tile(self._tile_type) and \
                override_cost is not None:
            raise ValueError("Cannot override cost of unknown specific tile.")
        self._specific_tile_generation_method: Optional[Callable[[], BaseTile]] = specific_tile_generation_method

        self._tile_requisites_override: Optional[List[TileTypeEnum]] = override_requisite
        self._tile_cost_override: Optional[Dict[ResourceTypeEnum, int]] = override_cost

        self._chosen_tile_generation_method: Optional[Callable[[], BaseTile]] = None
        self._tile_location: int = -1
        self._effects_to_use: Dict[BaseTilePurchaseEffect, int] = {}
        self._turn_descriptor: Optional[TurnDescriptorLookup] = None

        self._hash = self._precompute_hash()
        BaseAction.__init__(self, "PlaceASingleTileAction", True, False, False)

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("player cannot be none")

        if self._specific_tile_generation_method is not None:
            self._chosen_tile_generation_method = self._specific_tile_generation_method
        elif self._tile_service.does_tile_type_have_unique_tile(self._tile_type):
            self._chosen_tile_generation_method = self._tile_service \
                .get_unique_tile_generation_method(self._tile_type)
        else:
            possible_tiles: List[BaseTile] = self._tile_service \
                .get_possible_tiles(turn_descriptor.tiles, self._tile_type)
            specific_tile_to_build_result: ResultLookup[BaseTile] = player.get_player_choice_tile_to_build(
                possible_tiles,
                turn_descriptor)

            if not specific_tile_to_build_result.flag:
                self._chosen_tile_generation_method = lambda: None
                return ResultLookup(errors=specific_tile_to_build_result.errors)
            self._chosen_tile_generation_method = lambda: specific_tile_to_build_result.value

        primary_tile: BaseTile = self._chosen_tile_generation_method()

        location_to_build_result: ResultLookup[int] = player \
            .get_player_choice_location_to_build(
                primary_tile,
                turn_descriptor)

        if not location_to_build_result.flag:
            return ResultLookup(errors=location_to_build_result.errors)

        resources_from_constructing_tile_result: ResultLookup[Dict[ResourceTyeEnum, int]] = self._tile_service \
            .get_resources_taken_when_placing_tile_at_location(
                player,
                location_to_build_result.value)

        if not resources_from_constructing_tile_result.flag:
            return ResultLookup(errors=resources_from_constructing_tile_result.errors)

        self._tile_location = location_to_build_result.value

        should_get_effects_to_use_on_cost: bool = self._should_get_effects_to_use_on_cost(primary_tile)

        if should_get_effects_to_use_on_cost:
            # the flag for this result will never be false, because we're not passing any effects
            tile_cost_result: ResultLookup[Dict[ResourceTypeEnum, int]] = self._tile_service.get_cost_of_tile(
                primary_tile,
                self._tile_cost_override)

            possible_purchase_effects: List[BaseTilePurchaseEffect] = self._tile_service.get_purchase_effects(player, turn_descriptor.tiles)

            self._effects_to_use = player.get_player_choice_effects_to_use_for_cost_discount(
                tile_cost_result.value,
                possible_purchase_effects,
                turn_descriptor)
        else:
            self._effects_to_use = {}

        self._turn_descriptor = turn_descriptor

        if len(resources_from_constructing_tile_result.value) == 0:
            return ResultLookup(True, ActionChoiceLookup([]))

        receive_action = ReceiveAction(resources_from_constructing_tile_result.value)
        precedes_constraint = PrecedesConstraint(self, receive_action)

        return ResultLookup(True, ActionChoiceLookup([receive_action], [precedes_constraint]))

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
        if self._chosen_tile_generation_method is None:
            raise ValueError("Must choose a tile to place (_specific_tile_generation_method)")

        result: ResultLookup[int]
        errors: List[str] = []

        has_effects_result: ResultLookup[bool] = self._does_player_have_effects(player)

        errors.extend(has_effects_result.errors)

        chosen_tile: BaseTile = self._chosen_tile_generation_method()
        is_tile_available: bool = self._tile_service.is_tile_available(self._turn_descriptor, chosen_tile)
        can_place_tile_at_chosen_location: bool = self._tile_service.can_place_tile_at_location(
            player,
            chosen_tile,
            self._tile_location,
            self._tile_requisites_override)

        if not is_tile_available:
            errors.append(f"Tile ({chosen_tile.name}) has already been built")

        if not can_place_tile_at_chosen_location:
            errors.append(f"Chosen location {self._tile_location} is invalid")

        actual_cost_of_tile_result: ResultLookup[Dict[ResourceTypeEnum, int]] = self._tile_service.get_cost_of_tile(
            chosen_tile,
            self._tile_cost_override,
            self._effects_to_use)

        if not actual_cost_of_tile_result.flag:
            return ResultLookup(errors=actual_cost_of_tile_result.errors)

        can_player_afford_tile: bool = player.has_more_resources_than(actual_cost_of_tile_result.value)
        if not can_player_afford_tile:
            errors.append(CannotAffordActionError("Player", chosen_tile.name, actual_cost_of_tile_result.value, player.resources))

        success: bool = len(errors) == 0

        if not success:
            return ResultLookup(errors=errors)

        was_tile_placed_successfully_result: ResultLookup[bool] = self._tile_service.place_single_tile(
            player,
            chosen_tile,
            self._tile_location,
            self._tile_requisites_override)

        if not was_tile_placed_successfully_result.flag:
            return ResultLookup(errors=was_tile_placed_successfully_result.errors)

        success = player.take_resources(actual_cost_of_tile_result.value)

        for effect in chosen_tile.effects:
            if isinstance(effect, BaseOnPurchaseEffect):
                success &= effect.invoke(player)

        if not self._tile_service.does_tile_type_have_unique_tile(self._tile_type):
            self._turn_descriptor.tiles.remove(chosen_tile)

        result: ResultLookup[int] = ResultLookup(success, 1 if success else 0, errors)
        return result

    def new_turn_reset(self) -> None:
        self._tile_location = -1
        self._effects_to_use = {}
        self._chosen_tile_generation_method = None
        self._turn_descriptor = None

    def _should_get_effects_to_use_on_cost(
            self,
            primary_tile: BaseTile) -> bool:

        do_tiles_have_cost: bool = self._tile_cost_override is not None

        if not do_tiles_have_cost:
            primary_tile_cost_result: ResultLookup[Dict[ResourceTypeEnum, int]] = self._tile_service \
                .get_cost_of_tile(primary_tile)
            # Since we are not providing any effects, the flag will always be true
            primary_tile_cost: Dict[ResourceTypeEnum, int] = primary_tile_cost_result.value
            do_tiles_have_cost = any(primary_tile_cost[resource] for resource in primary_tile_cost)

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

    def __str__(self) -> str:
        tile_type_displayable: Dict[TileTypeEnum, str] = {
            TileTypeEnum.forest: "Forest",
            TileTypeEnum.underground: "Underground Tile",
            TileTypeEnum.meadow: "Meadow",
            TileTypeEnum.field: "Field",
            TileTypeEnum.cavern: "Cavern",
            TileTypeEnum.tunnel: "Tunnel",
            TileTypeEnum.deepTunnel: "Deep Tunnel",
            TileTypeEnum.pasture: "Pasture",
            TileTypeEnum.oreMine: "Ore Mine",
            TileTypeEnum.rubyMine: "Ruby Mine",
        }

        result: str
        cost: Dict[ResourceTypeEnum, int] = {}

        if self._specific_tile_generation_method is not None or self._tile_service.does_tile_type_have_unique_tile(self._tile_type):
            specific_tile: BaseTile = self._specific_tile_generation_method() \
                if self._specific_tile_generation_method is not None \
                else self._tile_service.get_unique_tile_generation_method(self._tile_type)()
            result = f"Place a {specific_tile.name}"

            cost = self._tile_service.get_cost_of_tile(specific_tile, self._tile_cost_override).value
        else:
            if self._tile_type is TileTypeEnum.furnishedCavern:
                result = "Furnish a cavern"
            elif self._tile_type is TileTypeEnum.furnishedDwelling:
                result = "Furnish a dwelling"
            else:
                result = f"Place a {tile_type_displayable[self._tile_type]}"

            if self._tile_cost_override is not None:
                cost = self._tile_cost_override

        if self._tile_requisites_override is not None:
            result += " on " + \
                " or ".join([tile_type_displayable[requisite] for requisite in self._tile_requisites_override]) \
                if len(self._tile_requisites_override) > 0 else \
                f" a {tile_type_displayable[self._tile_requisites_override[0]]}"

        if any(cost):
            result += " (for " + " and ".join([f"{amount} {resource.name}" for resource, amount in cost.items()]) + ")"

        return result

    def _precompute_hash(self) -> int:
        return hash(
            ("place single",
            self._tile_type,
            self._specific_tile_generation_method,
            *(self._tile_requisites_override if self._tile_requisites_override is not None else []),
            *(self._tile_cost_override.items() if self._tile_cost_override is not None else [])))

    def __hash__(self) -> int:
        return self._hash
