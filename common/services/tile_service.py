from __future__ import annotations

from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import List, Dict, Iterable, Tuple, Optional, Callable, cast, Self

from buisness_logic.effects.board_effects import ChangeRequisiteEffect
from buisness_logic.effects.purchase_effects import BaseTilePurchaseEffect
from buisness_logic.effects.receive_on_covering_effect import ReceiveOnCoveringEffect
from buisness_logic.tiles.mine_tiles import *
from buisness_logic.tiles.outdoor_tiles import *
from common.defaults.tile_requisite_default import TileRequisiteDefault
from common.defaults.tile_twin_default import TileTwinDefault
from common.entities.result_lookup import ResultLookup
from common.entities.tile_entity import TileEntity
from common.entities.tile_twin_placement_lookup import TileTwinPlacementLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_tile import BaseTile
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum, TileDirectionEnum


class LocationValidity(Enum):
    OtherSide = -1
    Invalid = 0
    Adjacent = 1
    Prerequisite = 2
    Valid = 3

    def __or__(self, other) -> LocationValidity:
        if self is LocationValidity.OtherSide or other is LocationValidity.OtherSide:
            return LocationValidity.OtherSide
        if self is LocationValidity.Invalid:
            return other
        if other is LocationValidity.Invalid:
            return self
        if self == other:
            return self
        # everything else either contains Valid, or is 'Adjacent | Prerequisite'
        return LocationValidity.Valid

    def __contains__(self, other):
        if other is LocationValidity.OtherSide:
            raise KeyError
        if self is LocationValidity.OtherSide:
            return False
        if other is LocationValidity.Invalid:
            return True
        if self == LocationValidity.Valid:
            return True
        if self == other:
            return True
        return False


class BaseValidLocations(metaclass=ABCMeta):
    @abstractmethod
    def ignore_requisites(self) -> None:
        raise NotImplemented()

    @abstractmethod
    def ignore_adjacency(self) -> None:
        raise NotImplemented()

    @abstractmethod
    def __contains__(self, item) -> bool:
        raise NotImplemented()

    @abstractmethod
    def minimum(self) -> int:
        raise NotImplemented()

    @abstractmethod
    def maximum(self) -> int:
        raise NotImplemented()

    @abstractmethod
    def __iter__(self):
        raise NotImplemented()

    @abstractmethod
    def __reversed__(self):
        raise NotImplemented()


class ValidLocations(BaseValidLocations):
    def __init__(self, source: List[LocationValidity]) -> None:
        self._source = source

    def ignore_requisites(self) -> None:
        self._source = [v | LocationValidity.Prerequisite for v in self._source]

    def ignore_adjacency(self) -> None:
        self._source = [v | LocationValidity.Adjacent for v in self._source]

    def __contains__(self, item) -> bool:
        return self._source[item] == LocationValidity.Valid

    def __iter__(self):
        return self._actually_valid_locations()

    def __reversed__(self):
        for location in range(len(self._source) - 1, -1, -1):
            if self._source[location] is LocationValidity.Valid:
                yield location

    def minimum(self) -> int:
        return min(self._actually_valid_locations())

    def maximum(self) -> int:
        return max(self._actually_valid_locations())

    def _actually_valid_locations(self):
        for (location, validity) in enumerate(self._source):
            if validity is LocationValidity.Valid:
                yield location


class TwinLocationValidity(object):
    def __init__(
            self,
            validity: LocationValidity = LocationValidity.Invalid,
            secondary_tiles: Optional[Dict[TileDirectionEnum, LocationValidity]] = None) -> None:
        self._primary_tile = validity
        self._secondary_tiles = {direction: LocationValidity.Invalid for direction in TileDirectionEnum} if secondary_tiles is None else secondary_tiles

    def __or__(self, validity) -> Self:
        # we are safe to use our own secondary_tiles without cloning because the user should avoid touching us again
        return TwinLocationValidity(self._primary_tile | validity, self._secondary_tiles)

    def __getitem__(self, direction) -> LocationValidity:
        '''Misuse! Gets whether a twin tile may point in the given direction, or the reason why not'''
        return self._secondary_tiles[direction]

    def __setitem__(self, direction, validity) -> None:
        self._secondary_tiles[direction] = validity

    def __contains__(self, direction) -> bool:
        '''Misuse! Returns whether the tile at the given location is valid'''
        return LocationValidity.Prerequisite in self._primary_tile and \
                LocationValidity.Prerequisite in self._secondary_tiles[direction] and \
                (LocationValidity.Adjacent in self._primary_tile or \
                    LocationValidity.Adjacent in self._secondary_tiles[direction])

    def __iter__(self):
        for direction in TileDirectionEnum:
            if direction in self:
                yield direction

    def are_any_directions_valid(self) -> bool:
        return any(direction in self for direction in TileDirectionEnum)

    def __repr__(self) -> str:
        return f"TwinLocationValidity({self._primary_tile}, {self._secondary_tiles!r})"


class ValidTwinTileLocations(BaseValidLocations):
    def __init__(self, source: List[LocationValidity]) -> None:
        self._tiles = [TwinLocationValidity(validity) for validity in source]

    def ignore_adjacency(self) -> None:
        self._tiles = [t | LocationValidity.Adjacent for t in self._tiles]

    def ignore_requisites(self) -> None:
        self._tiles = [t | LocationValidity.Prerequisite for t in self._tiles]

    def __getitem__(self, location) -> TwinLocationValidity:
        return self._tiles[location]

    def __setitem__(self, location, value) -> None:
        self._tiles[location] = value

    def __contains__(self, location: int | TileTwinPlacementLookup) -> bool:
        if type(location) is int:
            return self._tiles[location].are_any_directions_valid()
        return location.direction in self._tiles[location.location]

    def __iter__(self):
        for (location, twin_validity) in enumerate(self._tiles):
            if twin_validity.are_any_directions_valid():
                yield location

    def __reversed__(self):
        for location in range(len(self._tiles) - 1, -1, -1):
            if self._tiles[location].are_any_directions_valid():
                yield location

    def minimum(self) -> int:
        return min(self.__iter__())

    def maximum(self) -> int:
        return max(self.__iter__())


class TileService(object):
    def __init__(
            self,
            consider_unowned_tiles: bool = False) -> None:
        self._consider_unpurchased_tiles: bool = consider_unowned_tiles

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
            TileTypeEnum.oreMine: lambda: RubyMineTile(),
            TileTypeEnum.rubyMine: lambda: RubyMineTile(),
        }

        self._separable_twin_tile_funcs: Dict[TileTypeEnum, Tuple[Callable[[], BaseTile], Callable[[], BaseTile]]] = {
            TileTypeEnum.meadowFieldTwin: (MeadowTile, FieldTile),
            TileTypeEnum.cavernCavernTwin: (CavernTile, CavernTile),
            TileTypeEnum.cavernTunnelTwin: (CavernTile, TunnelTile),
            TileTypeEnum.oreMineDeepTunnelTwin: (OreMineTile, DeepTunnelTile),
        }

        self._inseparable_twin_tile_funcs: Dict[TileTypeEnum, Callable[[], BaseTile]] = {
            TileTypeEnum.pastureTwin: PastureTwinTile
        }

        self._direction_offset: Dict[TileDirectionEnum, Callable[[TileContainer], int]] = {
            TileDirectionEnum.up: lambda player: -player.width,
            TileDirectionEnum.down: lambda player: player.width,
            TileDirectionEnum.left: lambda _: -1,
            TileDirectionEnum.right: lambda _: 1}

        self._outdoor_tiles: List[TileTypeEnum] = [
            TileTypeEnum.forest,
            TileTypeEnum.meadow,
            TileTypeEnum.field,
            TileTypeEnum.meadowFieldTwin,
            TileTypeEnum.pasture,
            TileTypeEnum.pastureTwin,
        ]

        self._subset_tiles: Dict[TileTypeEnum, TileTypeEnum] = {
            TileTypeEnum.furnishedCavern: TileTypeEnum.furnishedDwelling
        }

    @property
    def outdoor_tiles(self) -> List[TileTypeEnum]:
        return self._outdoor_tiles

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

    def is_tile_placed_outside(
            self,
            tile_type: TileTypeEnum) -> bool:
        result: bool = tile_type in self._outdoor_tiles
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
        result: Tuple[Callable[[], BaseTile], Callable[[], BaseTile]]
        if tile_type in self._separable_twin_tile_funcs:
            result = self._separable_twin_tile_funcs[tile_type]
        elif tile_type in self._inseparable_twin_tile_funcs:
            inseparable_tile_to_build: BaseTile = self._inseparable_twin_tile_funcs[tile_type]()
            result = (lambda: inseparable_tile_to_build, lambda: inseparable_tile_to_build)
        else:
            raise ValueError(f"Tile with type {tile_type} does not have twin generation methods")

        return result

    def get_possible_tiles(
            self,
            tiles: List[BaseTile],
            tile_type: TileTypeEnum) -> List[BaseTile]:
        result: Dict[int, BaseTile] = {tile.id: tile for tile in tiles if tile.tile_type == tile_type}
        if tile_type in self._subset_tiles:
            additional_tiles: Dict[int, BaseTile] = {tile.id: tile for tile in self.get_possible_tiles(tiles, self._subset_tiles[tile_type])}
            result.update(additional_tiles)
        return list(result.values())

    def get_purchase_effects(
            self,
            player: TileContainer,
            unowned_tiles: List[BaseTile]) -> List[BaseTilePurchaseEffect]:
        possible_effects: List[BaseTilePurchaseEffect] = player.get_effects_of_type(BaseTilePurchaseEffect)
        if not self._consider_unpurchased_tiles:
            return possible_effects

        possible_effects.extend(
            effect for tile
            in self.get_possible_tiles(
                unowned_tiles,
                TileTypeEnum.furnishedCavern)
            for effect in tile.effects
            if isinstance(effect, BaseTilePurchaseEffect))

        return possible_effects

    def is_tile_available(
            self,
            turn_descriptor: TurnDescriptorLookup,
            tile: BaseTile) -> bool:
        if tile is None:
            raise ValueError("Tile may not be None")
        if tile.tile_type in self._unique_tile_funcs:
            return True
        if tile.tile_type in self._inseparable_twin_tile_funcs:
            return True
        for available_tile in turn_descriptor.tiles:
            if available_tile.id == tile.id:
                return True
        warnings.warn("cant find tile", tile, list(map(lambda x: x.name, turn_descriptor.tiles)))
        return False

    def can_place_tile_at_location(
            self,
            player: TileContainer,
            tile: BaseTile,
            location: int,
            requisites_override: Optional[List[TileTypeEnum]] = None) -> bool:
        """Gets whether or not a the given tile may be placed at the given location (and in the given direction) on the given player's board.

        :param player: The board where the tile will be placed. This may not be null.
        :param tile: The tile to be placed. This may not be null.
        :param location: The location to query whether the tile can be placed on. This must be positive, and less than the max size of the player's board.
        :param requisites_override: The requisites that the tile must be placed on. If this is null, the default will be used.
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

        tile_type_at_target_location: TileEntity = player.get_tile_at_location(location)

        result: bool
        if requisites_override is not None:
            result = tile_type_at_target_location.tile_type in requisites_override
        elif target_tile_type in self._tile_requisites:
            requisites_for_tile_type: List[TileTypeEnum] = self._tile_requisites[target_tile_type]
            result = tile_type_at_target_location.tile_type in requisites_for_tile_type
        else:
            # TODO: Implement? Could not find requisite tile type for given
            raise IndexError(f"Tile Type {target_tile_type} did not have any requisites")

        return result

    def can_place_twin_tile_at_location(
            self,
            player: TileContainer,
            twin_tile_type: TileTypeEnum,
            location: int,
            direction: TileDirectionEnum) -> bool:
        """Gets whether or not a the given tiles may be placed at the given location, and in the given direction, on the given player's board.

        :param player: The board where the tile will be placed. This may not be null.
        :param twin_tile_type: The type of the twin to be placed at the location. This may not be null.
        :param location: The location to query whether the tile can be placed on. This must be positive, and less than the max size of the player's board.
        :param direction: The direction to offset the section tile in.
        :returns: True if the tile may be placed at this location, false if not."""
        if player is None:
            raise ValueError("Player may not be None")
        if twin_tile_type not in self._twin_tile_types:
            raise ValueError("Tile type must be twin")
        if location < 0 or location >= player.tile_count:
            raise IndexError(f"Location index ({location}) must be in range [0, Number of Tiles owned by Player: {player.tile_count})")

        possible_locations: List[TileTwinPlacementLookup] = self \
            .get_available_locations_for_twin(
            player,
            twin_tile_type)

        result: bool = TileTwinPlacementLookup(location, direction) in possible_locations
        return result

    def get_resources_taken_when_placing_tile_at_location(
            self,
            player: TileContainer,
            location_to_build_tile: int) -> ResultLookup[Dict[ResourceTypeEnum, int]]:
        if player is None:
            raise ValueError("Player may not be None")
        if location_to_build_tile is None:
            raise ValueError("Location to build tile must not be None")

        primary_tile: TileEntity

        try:
            primary_tile = player.get_tile_at_location(location_to_build_tile)
        except IndexError as err:
            return ResultLookup(errors=err)

        resources: Dict[ResourceTypeEnum, int] = {}
        for effect in primary_tile.get_effects_of_type(ReceiveOnCoveringEffect):
            for (resource, amount) in effect.resources.items():
                resources[resource] = resources.get(resource, 0) + amount

        return ResultLookup(True, resources)

    def get_resources_taken_when_placing_twin_tile_at_location(
            self,
            player: TileContainer,
            location_to_build_tile: TileTwinPlacementLookup) -> ResultLookup[Dict[ResourceTypeEnum, int]]:
        if player is None:
            raise ValueError("Player may not be None")
        if location_to_build_tile is None:
            raise ValueError("Location to build tile must not be None")
        location, direction = location_to_build_tile
        location_of_secondary_tile: int = location + self._direction_offset[direction](player)

        primary_tile: TileEntity
        secondary_tile: TileEntity

        try:
            primary_tile = player.get_tile_at_location(location)
            secondary_tile = player.get_tile_at_location(location_of_secondary_tile)
        except IndexError as err:
            return ResultLookup(errors=err)

        resources: Dict[ResourceTypeEnum, int] = {}
        for effect in primary_tile.get_effects_of_type(ReceiveOnCoveringEffect):
            for (resource, amount) in effect.resources.items():
                resources[resource] = resources.get(resource, 0) + amount
        for effect in secondary_tile.get_effects_of_type(ReceiveOnCoveringEffect):
            for (resource, amount) in effect.resources.items():
                resources[resource] = resources.get(resource, 0) + amount

        return ResultLookup(True, resources)

    def get_cost_of_tile(
            self,
            tile: Optional[BaseTile] = None,
            cost_override: Optional[Dict[ResourceTypeEnum, int]] = None,
            effects_to_use: Optional[Dict[BaseTilePurchaseEffect, int]] = None) \
            -> ResultLookup[Dict[ResourceTypeEnum, int]]:
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
            tile_type: TileTypeEnum,
            requisites_override: Optional[List[TileTypeEnum]] = None) -> ValidLocations:
        """Get all locations available for a tile with the given type

        :param player: The player where the tile will be placed. This may not be null.
        :param tile_type: The type of the tile to be placed.
        :param requistes_override: The requisites that the tile must be placed on. If this is null, the default will be used.
        :returns: A list of locations. This will never be null.
        """
        if player is None:
            raise ValueError("Player may not be null")
        if self.is_tile_a_twin_tile(tile_type):
            raise ValueError("Tile is twin tile -- cannot be placed as single")

        tile_requisites: List[TileTypeEnum]
        if requisites_override is not None:
            tile_requisites = requisites_override
        elif tile_type is not None:
            all_tile_requisites: Dict[TileTypeEnum, List[TileTypeEnum]] = self._get_requisites_for_player(player)
            tile_requisites = all_tile_requisites[tile_type]
        else:
            raise ValueError("Both tile_type and requisites_override cannot be None")

        is_tile_placed_outside = self.is_tile_placed_outside(tile_type)

        valid_positions: List[LocationValidity] = [
                LocationValidity.Invalid
                    if self.is_tile_placed_outside(tile.tile_type) == is_tile_placed_outside and \
                        tile.tile_type != TileTypeEnum.unavailable
                    else LocationValidity.OtherSide
                for tile
                in player.tiles.values()]

        for location in player.tiles:
            location_tile_type: TileTypeEnum = player.tiles[location].tile_type
            if location_tile_type in tile_requisites:
                valid_positions[location] |= LocationValidity.Prerequisite

            adjacent_tile_locations: List[TileTwinPlacementLookup] = self.get_adjacent_tiles(player, location)
            is_tile_connected: bool = self._is_location_connected(player, location, adjacent_tile_locations)
            if is_tile_connected:
                valid_positions[location] |= LocationValidity.Adjacent

        return ValidLocations(valid_positions)

    def get_available_locations_for_twin(
            self,
            player: TileContainer,
            twin_tile_type: TileTypeEnum) -> ValidTwinTileLocations:
        """Get all locations available for a tile with the given type

        :param player: The player where the tile will be placed. This may not be null.
        :param twin_tile_type: The type of the twin tile to be placed. This may only be none if requisites_override is not none.
        :param requisites_override: The requisites that the tile must be placed on. If this is null, the default will be used.
        :returns: A list of locations and directions. This will never be null.
        """
        if player is None:
            raise ValueError("Player may not be null")

        all_tile_requisites: Dict[TileTypeEnum, List[TileTypeEnum]] = self._get_requisites_for_player(player)
        tile_requisites: List[TileTypeEnum] = all_tile_requisites[twin_tile_type]

        is_tile_placed_outside = self.is_tile_placed_outside(twin_tile_type)

        valid_locations = ValidTwinTileLocations(
            LocationValidity.Invalid
                if self.is_tile_placed_outside(tile.tile_type) == is_tile_placed_outside
                else LocationValidity.OtherSide
            for tile
            in player.tiles.values())

        for location in player.tiles:
            primary_location_tile_type: TileTypeEnum = player.tiles[location].tile_type

            if primary_location_tile_type in tile_requisites:
               valid_locations[location] |= LocationValidity.Prerequisite
            adjacent_tile_locations: List[TileTwinPlacementLookup] = self.get_adjacent_tiles(player, location)
            does_primary_tile_have_connected_adjacent_tiles: bool = self._is_location_connected(player, location, adjacent_tile_locations)

            is_location_connected: bool = does_primary_tile_have_connected_adjacent_tiles
            if does_primary_tile_have_connected_adjacent_tiles:
                valid_locations[location] |= LocationValidity.Adjacent

            for secondary_tile_location in adjacent_tile_locations:
                direction = secondary_tile_location.direction
                secondary_location_tile_type: TileTypeEnum = player.tiles[secondary_tile_location.location].tile_type

                if secondary_location_tile_type in tile_requisites:
                    valid_locations[location][direction] |= LocationValidity.Prerequisite
                if (primary_location_tile_type is TileTypeEnum.unavailable and \
                        secondary_location_tile_type is TileTypeEnum.unavailable):
                    valid_locations[location][direction] = LocationValidity.OtherSide

                adjacent_to_secondary_tile_locations: List[TileTwinPlacementLookup] = self.get_adjacent_tiles(
                    player,
                    secondary_tile_location.location)

                is_location_connected = self._is_location_connected(player, secondary_tile_location.location, adjacent_to_secondary_tile_locations)

                if is_location_connected:
                    valid_locations[location][direction] |= LocationValidity.Adjacent

        return valid_locations

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
            location: int,
            requisites_override: Optional[List[TileTypeEnum]] = None) -> ResultLookup[bool]:
        """Place a tile in this container

        :param player: The player who's board the tile will be placed on. This cannot be null.
        :param tile: The tile to be placed. This cannot be null.
        :param location: The location the tile should be placed. This cannot be null.
        :param requisites_override: The requisites that the tile must be placed on. If this is null, the default will be used.
        :returns: A result lookup indicating if the tile was successfully placed. This will never be null.
        """
        if player is None:
            raise ValueError("Player may not be null.")
        if tile is None:
            raise ValueError("base tile")
        if location < 0 or location > player.tile_count:
            raise ValueError("location must point to a valid position")

        available_locations: List[int] = self.get_available_locations_for_single(player, tile.tile_type, requisites_override)

        if location not in available_locations:
            location_validity = available_locations[location]
            return ResultLookup(errors=f"Cannot place {tile} at {location}: {location_validity}")

        player.tiles[location].set_tile(tile)

        result: ResultLookup[bool] = ResultLookup(True, True)
        return result

    def place_twin_tile(
            self,
            player: TileContainer,
            twin_tile_type: TileTypeEnum,
            primary_tile: BaseTile,
            secondary_tile: BaseTile,
            location: int,
            direction: TileDirectionEnum) -> ResultLookup[bool]:
        if player is None:
            raise ValueError("Player may not be None")
        if primary_tile is None:
            raise ValueError("Primary Tile may not be None")
        if secondary_tile is None:
            raise ValueError("Secondary Tile may not be None")
        if location < 0 or location >= player.tile_count:
            raise IndexError(f"Location index ({location}) must be in range [0, Number of Tiles owned by Player: {player.tile_count})")

        possible_locations: List[TileTwinPlacementLookup] = self.get_available_locations_for_twin(
            player,
            twin_tile_type)

        result: ResultLookup[bool]

        if TileTwinPlacementLookup(location, direction) in possible_locations:
            player.tiles[location].set_tile(primary_tile)

            location_of_secondary_tile: int = location + self._direction_offset[direction](player)
            player.tiles[location_of_secondary_tile].set_tile(secondary_tile)

            if twin_tile_type in self._inseparable_twin_tile_funcs:
                tile_as_twin: BaseTwinTile = cast(BaseTwinTile, primary_tile)
                tile_as_twin.place_tile(location, location_of_secondary_tile)

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

    def _is_location_connected(
            self,
            player: TileContainer,
            location: int,
            adjacent_tiles: List[TileTwinPlacementLookup]) -> bool:

        is_tile_connected: bool = False
        is_location_outside: bool = player.tiles[location].tile_type in self.outdoor_tiles

        for adjacent_tile_location in adjacent_tiles:
            adjacent_location_tile_type: TileTypeEnum = player.tiles[adjacent_tile_location.location].tile_type
            is_adjacent_location_outside: bool = adjacent_location_tile_type in self.outdoor_tiles

            can_connection_be_made_through_adjacent_tile: bool
            if is_location_outside and is_adjacent_location_outside:
                can_connection_be_made_through_adjacent_tile = adjacent_location_tile_type != TileTypeEnum.forest and \
                                                               adjacent_location_tile_type != TileTypeEnum.unavailable
            elif not is_location_outside and not is_adjacent_location_outside:
                can_connection_be_made_through_adjacent_tile = adjacent_location_tile_type != TileTypeEnum.underground and \
                                                               adjacent_location_tile_type != TileTypeEnum.unavailable
            else:
                can_connection_be_made_through_adjacent_tile = location == 35 and adjacent_tile_location.location == 36 or \
                                                               location == 36 and adjacent_tile_location.location == 35

            if can_connection_be_made_through_adjacent_tile:
                is_tile_connected = True
                break

        return is_tile_connected
