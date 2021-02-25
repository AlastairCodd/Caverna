from typing import List, Optional, Callable, Dict

from buisness_logic.effects.base_effects import BaseOnPurchaseEffect
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.tile_unknown_placement_lookup import TileUnknownPlacementLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from common.services.tile_service import TileService
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_player_choice_action import BasePlayerChoiceAction
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import TileTypeEnum, TileDirectionEnum
from core.repositories.base_player_repository import BasePlayerRepository
from core.services.base_player_service import BasePlayerService


class PlaceATwinTileAction(BasePlayerChoiceAction):
    def __init__(
            self,
            tile_type: TileTypeEnum):
        self._tile_service: TileService = TileService()

        self._tile_type: TileTypeEnum = tile_type
        if not self._tile_service.is_tile_a_twin_tile(self._tile_type):
            raise ValueError("Tile type must be twin")

        self._primary_twin_tile_generation_method: Optional[Callable[[], BaseTile]] = None
        self._secondary_twin_tile_generation_method: Optional[Callable[[], BaseTile]] = None

        self._tile_location: int = -1
        self._tile_direction: Optional[TileDirectionEnum] = None
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
        self._turn_descriptor = None

    def __str__(self) -> str:
        tile_type_displayable: Dict[TileTypeEnum,str] = {
            TileTypeEnum.pastureTwin: "Twin Pasture",
            TileTypeEnum.cavernTunnelTwin: "Cavern Tunnel Twin",
            TileTypeEnum.cavernCavernTwin: "Twin Cavern",
            TileTypeEnum.oreMineDeepTunnelTwin: "Ore Mine and Deep Tunnel",
            TileTypeEnum.meadowFieldTwin: "Meadow and Field pair",
        }

        return f"Place a {tile_type_displayable[self._tile_type]}"
