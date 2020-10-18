from typing import List, Union, Dict, Iterable, Tuple, Optional, Callable

from buisness_logic.effects.board_effects import ChangeRequisiteEffect
from buisness_logic.effects.purchase_effects import BaseTilePurchaseEffect
from buisness_logic.tiles.outdoor_tiles import *
from common.defaults.tile_requisite_default import TileRequisiteDefault
from common.defaults.tile_twin_default import TileTwinDefault
from core.baseClasses.base_effect import BaseEffect
from core.repositories.base_player_repository import BasePlayerRepository
from common.entities.result_lookup import ResultLookup
from common.entities.tile_entity import TileEntity
from core.baseClasses.base_tile import BaseTile
from core.containers.resource_container import ResourceContainer
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum, TileDirectionEnum


class TileService(object):
    def __init__(self):
        requisite_default: TileRequisiteDefault = TileRequisiteDefault()
        self._tileRequisites: Dict[TileTypeEnum, List[TileTypeEnum]] = requisite_default.assign({})

        twin_default: TileTwinDefault = TileTwinDefault()
        self._twinTiles: List[TileTypeEnum] = twin_default.assign([])

        self._unique_tile_funcs: Dict[TileTypeEnum, Callable[[], BaseTile]] = {
            TileTypeEnum.field: lambda: FieldTile(),
            TileTypeEnum.meadow: lambda: MeadowTile(),
            TileTypeEnum.meadowFieldTwin: lambda: MeadowTile(),
            TileTypeEnum.pasture: lambda: PastureTile(),
        }

    # TODO Implement and test this service
    def is_tile_a_twin_tile(
            self,
            tile_type: TileTypeEnum) -> bool:
        result: bool = tile_type in self._twinTiles
        return result

    def does_tile_type_have_unique_tile(
            self,
            tile_type: TileTypeEnum) -> bool:
        result: bool = tile_type in self._unique_tile_funcs
        return result

    def get_unique_tile_generation_method(
            self,
            tile_type: TileTypeEnum) -> Optional[Callable[[], BaseTile]]:
        """Gets the unique BaseTile associated with the given TileType, if one exists.

        :param tile_type: The type of the tile to get the BaseTile for.
        :returns: The specific base tile associated with the tile type. This may be null, if the tile is not unique."""
        result: Optional[Callable[[], BaseTile]]
        if tile_type in self._unique_tile_funcs:
            result = self._unique_tile_funcs[tile_type]
        else:
            result = None
        return result

    def get_possible_tiles(
            self,
            tiles: List[BaseTile],
            tile_type: TileTypeEnum) -> List[BaseTile]:
        result: List[BaseTile] = [tile for tile in tiles if tile.tile_type == tile_type]
        return result

    # TODO: consider how to get this singleton information out
    def is_tile_available(
            self,
            tile: BaseTile) -> bool:
        pass

    def can_place_tile_at_location(
            self,
            player: TileContainer,
            tile: BaseTile,
            location: int,
            direction: Union[TileDirectionEnum, None]) -> bool:
        """Gets whether or not a the given tile may be placed at the given location (and in the given direction) on the given player's board.

        :param player: The board where the tile will be placed. This may not be null.
        :param tile: The tile to be placed. This may not be null.
        :param location: The location to query whether the tile can be placed on. This must be positive, and less than the max size of the player's board.
        :param direction: The direction of the tile, if it is a twin tile. Iff the tile is a twin tile, this may not be null.
        :returns: True if the tile may be placed at this location, false if not."""
        # TODO: implement this
        pass

    def get_cost_of_tile(
            self,
            tile: BaseTile,
            effects_to_use: Optional[Dict[BaseTilePurchaseEffect, int]] = None,
            cost_override: Optional[Dict[ResourceTypeEnum, int]] = None) -> ResultLookup[Dict[ResourceTypeEnum, int]]:
        """Gets the cost to the given player to build the given tile.

        :param tile: The tile to be built. This may not be null.
        :param effects_to_use: The effects that the player who aims to build the tile may use, which could reduce the building cost. If null, no effects will be used.
        :param cost_override: The cost to use in place of the default tile cost. This may be null.
        :returns: The cost to build the tile. This will never be null."""
        if tile is None:
            raise ValueError("Tile may not be null")

        tile_cost: Dict[ResourceTypeEnum, int]
        if cost_override is None:
            tile_cost = dict(tile.cost)
        else:
            tile_cost = dict(cost_override)

        result: ResultLookup[Dict[ResourceTypeEnum, int]]

        if effects_to_use is not None:
            effect: BaseTilePurchaseEffect
            for effect in effects_to_use:
                for _ in range(effects_to_use[effect]):
                    tile_cost = effect.invoke(tile_cost)

            errors: List[str] = []
            for resource in tile_cost:
                if tile_cost[resource] < 0:
                    errors.append(f"Reduced cost of {resource} too much (resultant cost was less than zero)")
            result = ResultLookup(len(errors) == 0, tile_cost, errors)
        else:
            result = ResultLookup(True, tile_cost)

        return result

    def get_available_locations(
            self,
            player: TileContainer,
            tile_type: TileTypeEnum) -> List[Tuple[int, Union[TileDirectionEnum, None]]]:
        """Get all locations available for a tile with the given type

        :param player: The player where the tile will be placed. This may not be null.
        :param tile_type: The type of the tile to be placed.
        :returns: A list of locations (and directions, if the tile_type is for a twin tile). This will never be null.
        """
        effects: Iterable[ChangeRequisiteEffect] = player.get_effects_of_type(ChangeRequisiteEffect)

        # gotta clone dictionary
        all_tile_requisites: Dict[TileTypeEnum, List[TileTypeEnum]] = dict(self._tileRequisites)

        for effect in effects:
            effect.invoke(all_tile_requisites)

        # get the correct requisites -- if adjacent, allow unavailable
        tile_requisites: List[TileTypeEnum] = all_tile_requisites[tile_type]

        # filter _tilesType by new requisites
        x: Tuple[int, TileEntity]
        valid_positions: List[Tuple[int, Optional[TileDirectionEnum]]] = [(x[0], None) for x in player.tiles.items() if x[1].tile_type in tile_requisites]

        # if twin, check all requisites for adjacent
        if not self.is_tile_a_twin_tile(tile_type):
            return valid_positions

        valid_positions_with_adjacent: List[Tuple[int, Optional[TileDirectionEnum]]] = []
        for position in valid_positions:
            adjacent_tile_locations: List[Tuple[int, TileDirectionEnum]] = self.get_adjacent_tiles(player, position[0])
            for adjacentTile in adjacent_tile_locations:
                adjacent_tile_type: TileTypeEnum = player.tiles[adjacentTile[0]].tile_type
                if adjacent_tile_type in tile_requisites:
                    new_entry: Tuple[int, Optional[TileDirectionEnum]] = (position[0], adjacentTile[1])
                    valid_positions_with_adjacent.append(new_entry)
                    break

        return valid_positions_with_adjacent

    def get_adjacent_tiles(
            self,
            player: TileContainer,
            location: int) -> List[Tuple[int, TileDirectionEnum]]:
        if location < 0 or location > player.tile_count:
            raise ValueError(f"location must be between 0 and number of tiles (value: {location}")

        result: List[Tuple[int, TileDirectionEnum]] = []

        adjacent_direction_condition: Dict[TileDirectionEnum, Callable[[int], bool]] = {
            TileDirectionEnum.up: lambda x_adjacent_location: x_adjacent_location > 0,
            TileDirectionEnum.down: lambda x_adjacent_location: x_adjacent_location < player.tile_count,
            TileDirectionEnum.left: lambda x_adjacent_location: x_adjacent_location % player.width != 7,
            TileDirectionEnum.right: lambda x_adjacent_location: x_adjacent_location % player.width != 0}

        direction_offset: Dict[TileDirectionEnum, int] = {
            TileDirectionEnum.up: -player.width,
            TileDirectionEnum.down: player.width,
            TileDirectionEnum.left: -1,
            TileDirectionEnum.right: 1}

        direction: TileDirectionEnum
        for direction in direction_offset:
            adjacent_location: int = location + direction_offset[direction]
            if adjacent_direction_condition[direction](adjacent_location):
                result.append((adjacent_location, direction))

        return result

    def place_tile(
            self,
            player: TileContainer,
            tile: BaseTile,
            location: int,
            direction: Optional[TileDirectionEnum] = None) -> ResultLookup[bool]:
        """Place a tile in this container

            :param player: The player who's board the tile will be placed on. This cannot be null.
            :param tile: The tile to be placed. This cannot be null.
            :param location: The location the tile should be placed. This cannot be null.
            :param direction: The direction a double tile points. This cannot be null if the given tile is a twin tile.
            :returns: A result lookup indicating if the tile was successfully placed. This will never be null.
        """
        if player is None:
            raise ValueError("Player may not be null.")
        if tile is None:
            raise ValueError("base tile")
        if location < 0 or location > player.tile_count:
            raise ValueError("location must point to a valid position")
        if self.is_tile_a_twin_tile(tile.tile_type) and direction is None:
            raise ValueError("Direction cannot be null if tile is a twin tile")

        tile_type = TileTypeEnum.furnishedDwelling if tile.is_dwelling else TileTypeEnum.furnishedCavern

        available_locations: List[Tuple[int, Optional[TileDirectionEnum]]] = self.get_available_locations(player, tile_type)

        success: bool = False
        errors: List[str] = []

        if location in available_locations:
            player.tiles[location].set_tile(tile)
            success = True

        result: ResultLookup[bool] = ResultLookup(success, success, errors)
        return result
