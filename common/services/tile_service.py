from typing import List, Union, Dict, Iterable, Tuple, Optional, Callable

from buisness_logic.effects.board_effects import ChangeRequisiteEffect
from buisness_logic.effects.purchase_effects import BaseTilePurchaseEffect
from buisness_logic.tiles.mine_tiles import *
from buisness_logic.tiles.outdoor_tiles import *
from common.defaults.tile_requisite_default import TileRequisiteDefault
from common.defaults.tile_twin_default import TileTwinDefault
from common.entities.result_lookup import ResultLookup
from common.entities.tile_entity import TileEntity
from common.entities.tile_twin_placement_lookup import TileTwinPlacementLookup
from core.baseClasses.base_tile import BaseTile
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum, TileDirectionEnum


class TileService(object):
    def __init__(self):
        requisite_default: TileRequisiteDefault = TileRequisiteDefault()
        self._tile_requisites: Dict[TileTypeEnum, List[TileTypeEnum]] = {}
        requisite_default.assign(self._tile_requisites)

        twin_default: TileTwinDefault = TileTwinDefault()
        self._twin_tile_types: List[TileTypeEnum] = []
        twin_default.assign(self._twin_tile_types)

        self._unique_tile_funcs: Dict[TileTypeEnum, Callable[[], BaseTile]] = {
            TileTypeEnum.field: lambda: FieldTile(),
            TileTypeEnum.meadow: lambda: MeadowTile(),
            TileTypeEnum.pasture: lambda: PastureTile(),
            TileTypeEnum.cavern: lambda: CavernTile(),
            TileTypeEnum.tunnel: lambda: TunnelTile(),
            TileTypeEnum.deepTunnel: lambda: DeepTunnelTile(),
            TileTypeEnum.rubyMine: lambda: RubyMineTile(),
        }

        self._twin_tile_funcs: Dict[TileTypeEnum, Tuple[Callable[[], BaseTile], Callable[[], BaseTile]]] = {
            TileTypeEnum.meadowFieldTwin: (MeadowTile, FieldTile),
            TileTypeEnum.cavernCavernTwin: (CavernTile, CavernTile),
            TileTypeEnum.cavernTunnelTwin: (CavernTile, TunnelTile),
            TileTypeEnum.oreMineDeepTunnelTwin: (OreMineTile, DeepTunnelTile),
        }

        self._direction_offset: Dict[TileDirectionEnum, Callable[[TileContainer], int]] = {
            TileDirectionEnum.up: lambda player: -player.width,
            TileDirectionEnum.down: lambda player: player.width,
            TileDirectionEnum.left: lambda _: -1,
            TileDirectionEnum.right: lambda _: 1}

    # TODO Implement and test this service
    def is_tile_a_twin_tile(
            self,
            tile_type: TileTypeEnum) -> bool:
        result: bool = tile_type in self._twin_tile_types
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

    def get_twin_tile_generation_methods(
            self,
            tile_type: TileTypeEnum) -> Tuple[Callable[[], BaseTile], Callable[[], BaseTile]]:
        if tile_type not in self._twin_tile_funcs:
            raise ValueError(f"Tile with type {tile_type} does not have twin generation methods")
        result: Tuple[Callable[[], BaseTile], Callable[[], BaseTile]] = self._twin_tile_funcs[tile_type]
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
        if tile is None:
            raise ValueError("Tile may not be None")
        return True

    def can_place_tile_at_location(
            self,
            player: TileContainer,
            tile: BaseTile,
            location: int) -> bool:
        """Gets whether or not a the given tile may be placed at the given location (and in the given direction) on the given player's board.

        :param player: The board where the tile will be placed. This may not be null.
        :param tile: The tile to be placed. This may not be null.
        :param location: The location to query whether the tile can be placed on. This must be positive, and less than the max size of the player's board.
        :returns: True if the tile may be placed at this location, false if not."""
        if player is None:
            raise ValueError("Player may not be None")
        if tile is None:
            raise ValueError("Tile may not be None")
        if location < 0 or location >= player.tile_count:
            raise IndexError(f"Location index ({location}) must be in range [0, Number of Tiles owned by Player: {player.tile_count})")
        target_tile_type: TileTypeEnum = tile.tile_type
        is_tile_a_twin_tile = self.is_tile_a_twin_tile(target_tile_type)
        if is_tile_a_twin_tile:
            raise ValueError(f"Tile {target_tile_type} is a twin tile.")

        result: bool
        if target_tile_type in self._tile_requisites:
            requisites_for_tile_type: List[TileTypeEnum] = self._tile_requisites[target_tile_type]
            tile_type_at_target_location: TileEntity = player.get_tile_at_location(location)
            result = tile_type_at_target_location.tile_type in requisites_for_tile_type
        else:
            # TODO: Implement? Could not find requisite tile type for given
            raise IndexError(f"Tile Type {target_tile_type} did not have any requisites")

        return result

    def can_place_twin_tile_at_location(
            self,
            player: TileContainer,
            primary_tile: BaseTile,
            secondary_tile: BaseTile,
            location: int,
            direction: TileDirectionEnum) -> bool:
        """Gets whether or not a the given tiles may be placed at the given location, and in the given direction, on the given player's board.

        :param player: The board where the tile will be placed. This may not be null.
        :param primary_tile: The tile to be placed at the location. This may not be null.
        :param secondary_tile: The tile to be placed, offset from the location in the given direction. This may not be null.
        :param location: The location to query whether the tile can be placed on. This must be positive, and less than the max size of the player's board.
        :param direction: The direction to offset the section tile in.
        :returns: True if the tile may be placed at this location, false if not."""
        if player is None:
            raise ValueError("Player may not be None")
        if primary_tile is None:
            raise ValueError("Primary Tile may not be None")
        if secondary_tile is None:
            raise ValueError("Seconday Tile may not be None")
        if location < 0 or location >= player.tile_count:
            raise IndexError(f"Location index ({location}) must be in range [0, Number of Tiles owned by Player: {player.tile_count})")

        possible_locations: List[TileTwinPlacementLookup] = self.get_available_locations_for_twin(player, primary_tile.tile_type, secondary_tile.tile_type)
        result: bool = TileTwinPlacementLookup(location, direction) in possible_locations
        return result

    def get_cost_of_tile(
            self,
            tile: Optional[BaseTile] = None,
            cost_override: Optional[Dict[ResourceTypeEnum, int]] = None,
            effects_to_use: Optional[Dict[BaseTilePurchaseEffect, int]] = None) -> ResultLookup[Dict[ResourceTypeEnum, int]]:
        """Gets the cost to the given player to build the given tile.

        :param tile: The tile to be built. This may be null, if cost override is not null.
        :param effects_to_use: The effects that the player who aims to build the tile may use, which could reduce the building cost.
            If null, no effects will be used.
        :param cost_override: The cost to use in place of the default tile cost. This may be null, if tile is not null.
        :returns: The cost to build the tile. This will never be null."""
        if tile is None and cost_override is None:
            raise ValueError("At least one of tile and cost_override may not be null")

        tile_cost: Dict[ResourceTypeEnum, int]
        if cost_override is None:
            tile_cost = dict(tile.cost)
        else:
            tile_cost = dict(cost_override)

        result: ResultLookup[Dict[ResourceTypeEnum, int]]

        if effects_to_use is not None and len(effects_to_use) > 0:
            effect: BaseTilePurchaseEffect
            for effect in effects_to_use:
                for _ in range(effects_to_use[effect]):
                    tile_cost = effect.invoke(tile_cost)

            errors: List[str] = []
            resources_to_remove: List[ResourceTypeEnum] = []
            for resource in tile_cost:
                cost_for_resource: int = tile_cost[resource]
                if cost_for_resource < 0:
                    errors.append(f"Reduced cost of {resource} too much (resultant cost was less than zero)")
                if cost_for_resource == 0:
                    resources_to_remove.append(resource)

            for resource in resources_to_remove:
                tile_cost.pop(resource)
            result = ResultLookup(len(errors) == 0, tile_cost, errors)
        else:
            result = ResultLookup(True, tile_cost)

        return result

    def get_available_locations_for_single(
            self,
            player: TileContainer,
            tile_type: TileTypeEnum) -> List[int]:
        """Get all locations available for a tile with the given type

        :param player: The player where the tile will be placed. This may not be null.
        :param tile_type: The type of the tile to be placed.
        :returns: A list of locations. This will never be null.
        """
        if player is None:
            raise ValueError("Player may not be null")
        if self.is_tile_a_twin_tile(tile_type):
            raise ValueError("Tile is twin tile -- cannot be placed as single")

        all_tile_requisites: Dict[TileTypeEnum, List[TileTypeEnum]] = self._get_requisites_for_player(player)
        tile_requisites: List[TileTypeEnum] = all_tile_requisites[tile_type]
        valid_positions: List[int] = [location for location in player.tiles if player.tiles[location].tile_type in tile_requisites]

        return valid_positions

    def get_available_locations_for_twin(
            self,
            player: TileContainer,
            primary_tile_type: TileTypeEnum,
            secondary_tile_type: TileTypeEnum) -> List[TileTwinPlacementLookup]:
        """Get all locations available for a tile with the given type

        :param player: The player where the tile will be placed. This may not be null.
        :param primary_tile_type: The type of the tile to be placed.
        :param secondary_tile_type: The type of the tile to be placed.
        :returns: A list of locations and directions. This will never be null.
        """
        if player is None:
            raise ValueError("Player may not be null")
        all_tile_requisites: Dict[TileTypeEnum, List[TileTypeEnum]] = self._get_requisites_for_player(player)

        # get the correct requisites -- if adjacent, allow unavailable
        primary_tile_requisites: List[TileTypeEnum] = all_tile_requisites[primary_tile_type]
        secondary_tile_requisites: List[TileTypeEnum] = all_tile_requisites[secondary_tile_type]

        valid_positions_with_adjacent: List[TileTwinPlacementLookup] = []

        for location in player.tiles:
            if player.tiles[location].tile_type in primary_tile_requisites:
                adjacent_tile_locations: List[TileTwinPlacementLookup] = self.get_adjacent_tiles(player, location)
                for adjacentTile in adjacent_tile_locations:
                    adjacent_tile_type: TileTypeEnum = player.tiles[adjacentTile[0]].tile_type
                    if adjacent_tile_type in secondary_tile_requisites:
                        valid_positions_with_adjacent.append(TileTwinPlacementLookup(location, adjacentTile[1]))
                        break

        return valid_positions_with_adjacent

    def get_adjacent_tiles(
            self,
            player: TileContainer,
            location: int) -> List[TileTwinPlacementLookup]:
        if location < 0 or location > player.tile_count:
            raise ValueError(f"location must be between 0 and number of tiles (value: {location}")

        adjacent_direction_condition: Dict[TileDirectionEnum, Callable[[int], bool]] = {
            TileDirectionEnum.up: lambda x_adjacent_location: x_adjacent_location > 0,
            TileDirectionEnum.down: lambda x_adjacent_location: x_adjacent_location < player.tile_count,
            TileDirectionEnum.left: lambda x_adjacent_location: x_adjacent_location % player.width != 7,
            TileDirectionEnum.right: lambda x_adjacent_location: x_adjacent_location % player.width != 0}

        result: List[TileTwinPlacementLookup] = [
            TileTwinPlacementLookup(location + self._direction_offset[direction](player), direction)
            for direction in self._direction_offset
            if adjacent_direction_condition[direction](location + self._direction_offset[direction](player))]

        # result: List[TileTwinPlacementLookup] = []
        # direction: TileDirectionEnum
        #
        # for direction in direction_offset:
        #     adjacent_location: int = location + direction_offset[direction]
        #     if adjacent_direction_condition[direction](adjacent_location):
        #         result.append((adjacent_location, direction))

        return result

    def place_single_tile(
            self,
            player: TileContainer,
            tile: BaseTile,
            location: int) -> ResultLookup[bool]:
        """Place a tile in this container

            :param player: The player who's board the tile will be placed on. This cannot be null.
            :param tile: The tile to be placed. This cannot be null.
            :param location: The location the tile should be placed. This cannot be null.
            :returns: A result lookup indicating if the tile was successfully placed. This will never be null.
        """
        if player is None:
            raise ValueError("Player may not be null.")
        if tile is None:
            raise ValueError("base tile")
        if location < 0 or location > player.tile_count:
            raise ValueError("location must point to a valid position")

        available_locations: List[int] = self.get_available_locations_for_single(player, tile.tile_type)

        success: bool = False
        errors: List[str] = []

        if location in available_locations:
            player.tiles[location].set_tile(tile)
            success = True
        else:
            errors.append(f"Invalid location {location}")

        result: ResultLookup[bool] = ResultLookup(success, success, errors)
        return result

    def place_twin_tile(
            self,
            player: TileContainer,
            primary_tile: BaseTile,
            secondary_tile: BaseTile,
            location: int,
            direction: TileDirectionEnum) -> ResultLookup[bool]:
        if player is None:
            raise ValueError("Player may not be None")
        if primary_tile is None:
            raise ValueError("Primary Tile may not be None")
        if secondary_tile is None:
            raise ValueError("Seconday Tile may not be None")
        if location < 0 or location >= player.tile_count:
            raise IndexError(f"Location index ({location}) must be in range [0, Number of Tiles owned by Player: {player.tile_count})")

        possible_locations: List[TileTwinPlacementLookup] = self.get_available_locations_for_twin(player, primary_tile.tile_type, secondary_tile.tile_type)

        result: ResultLookup[bool]

        if TileTwinPlacementLookup(location, direction) in possible_locations:
            player.tiles[location].set_tile(primary_tile)

            location_of_secondary_tile: int = location + self._direction_offset[direction](player)
            player.tiles[location_of_secondary_tile].set_tile(secondary_tile)
            result = ResultLookup(True, True)
        else:
            result = ResultLookup(errors=f"Chosen position ({location}, {direction.name}) are invalid")

        return result

    def _get_requisites_for_player(
            self,
            player: TileContainer) -> Dict[TileTypeEnum, List[TileTypeEnum]]:
        if player is None:
            raise ValueError("Player may not be none")

        effects: Iterable[ChangeRequisiteEffect] = player.get_effects_of_type(ChangeRequisiteEffect)
        all_tile_requisites: Dict[TileTypeEnum, List[TileTypeEnum]] = dict(self._tile_requisites)

        for effect in effects:
            effect.invoke(all_tile_requisites)

        return all_tile_requisites
