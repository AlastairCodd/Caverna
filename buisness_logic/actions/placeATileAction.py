from typing import List, Dict, Tuple, Optional

from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService
from common.entities.result_lookup import ResultLookup
from common.services.tile_service import TileService
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum, TileDirectionEnum
from core.enums.harvest_type_enum import HarvestTypeEnum


class PlaceATileAction(BasePlayerChoiceAction):
    def __init__(
            self,
            tile_type: TileTypeEnum,
            specific_tile: Optional[BaseTile] = None,
            override_cost: Optional[Dict[ResourceTypeEnum, int]] = None):
        self._tile_service: TileService = TileService()

        self._tile_type: TileTypeEnum = tile_type

        self._tile_location: int = -1
        self._tile_direction: Optional[TileDirectionEnum] = None
        self._specific_tile: Optional[BaseTile] = specific_tile

        self._tile_cost_override: Optional[Dict[ResourceTypeEnum, int]] = override_cost

    def set_player_choice(
            self,
            player: BasePlayerService,
            dwarf: Dwarf,
            cards: List[BaseCard],
            turn_index: int,
            round_index: int,
            harvest_type: HarvestTypeEnum) -> ResultLookup[ActionChoiceLookup]:
        if player is None:
            raise ValueError("player cannot be none")

        success: bool = True
        errors: List[str] = []

        if self._specific_tile is None:
            does_tile_have_unique_type: bool = self._tile_service.does_tile_type_have_unique_tile(self._tile_type)

            if does_tile_have_unique_type:
                self._specific_tile = self._tile_service.get_unique_tile(self._tile_type)
            else:
                possible_tiles: List[BaseTile] = self._tile_service.get_possible_tiles(self._tile_type)
                specific_tile_to_build_result: ResultLookup[BaseTile] = player.get_player_choice_tile_to_build(
                    possible_tiles,
                    turn_index,
                    round_index,
                    harvest_type)

                success = specific_tile_to_build_result.flag
                errors.extend(specific_tile_to_build_result.errors)

                if specific_tile_to_build_result.flag:
                    self._specific_tile = specific_tile_to_build_result.value

        if success:
            # TODO: Make this value a type
            location_to_build_result: ResultLookup[Tuple[int, TileDirectionEnum]] = player.get_player_choice_location_to_build(
                self._specific_tile,
                turn_index,
                round_index,
                harvest_type)

            success = location_to_build_result.flag
            errors.extend(location_to_build_result.errors)

            if location_to_build_result.flag:
                self._tile_location = location_to_build_result.value[0]
                self._tile_direction = location_to_build_result.value[1]

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
        if self._specific_tile is None:
            raise ValueError("Must choose a tile to place")

        is_tile_available: bool = self._tile_service.is_tile_available(self._specific_tile)
        can_player_afford_tile: bool = self._tile_service.can_player_afford_to_build_tile(
            player,
            self._specific_tile,
            self._tile_cost_override)
        can_place_tile_at_chosen_location: bool = self._tile_service.can_place_tile_at_location(
            player,
            self._specific_tile,
            self._tile_location,
            self._tile_direction)

        errors: List[str] = []

        if not is_tile_available:
            errors.append("Tile has already been built")
        if not can_player_afford_tile:
            cost_of_tile: Dict[ResourceTypeEnum, int]
            if self._tile_cost_override is not None:
                cost_of_tile = self._tile_cost_override
            else:
                cost_of_tile = self._tile_service.get_cost_of_tile(
                    player,
                    self._specific_tile)

            errors.append(f"Player cannot afford tile (cost: {cost_of_tile}, player resources: {player.resources})")
        if not can_place_tile_at_chosen_location:
            errors.append(f"Chosen location {self._tile_location} is invalid")

        success: bool = len(errors) == 0

        if success:
            was_tile_placed_successfully_result: ResultLookup[bool] = self._tile_service.place_tile(
                player,
                self._specific_tile,
                self._tile_location,
                self._tile_direction)

            success = was_tile_placed_successfully_result.flag
            errors.extend(was_tile_placed_successfully_result.errors)

        result: ResultLookup[int] = ResultLookup(success, 1 if success else 0, errors)
        return result

    def new_turn_reset(self) -> None:
        self._tile_location = -1
        self._specific_tile = None
        self._tile_direction = None
