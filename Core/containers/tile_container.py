from typing import List, Tuple, Dict, TypeVar, Generic, Iterable

from buisness_logic.effects.board_effects import ChangeRequisiteEffect
from common.entities.tile_entity import TileEntity
from core.enums.caverna_enums import TileDirectionEnum, TileTypeEnum
from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile
from common.defaults import tile_container_default, tile_twin_default, tile_requisite_default

T = TypeVar('T')

class TileContainer(object):

    def __init__(self, height=6, width=8):
        if height < 0:
            raise ValueError("height must be greater than 0")
        if width < 0:
            raise ValueError("width must be greater than 0")
        self._height = height
        self._width = width

        self._tileCount = height * width

        twin_default = tile_twin_default.TileTwinDefault()
        self._twinTiles = twin_default.assign([])

        self._tiles: Dict[int, TileEntity] = {}
        if height == 6 and width == 8:
            default = tile_container_default.TileContainerDefault()
            default.assign(self._tiles)

        requisite_default = tile_requisite_default.TileRequisiteDefault()
        self._tileRequisites: Dict[TileTypeEnum, List[TileTypeEnum]] = requisite_default.assign({})

    def get_number_of_tiles_of_type(self, tile_type: TileTypeEnum) -> int:
        return len([t for t in self._tiles.values() if t.get_tile_type() == tile_type])

    def get_tiles(self) -> List[BaseTile]:
        """Get the base tiles contained in this container"""
        result = [x.get_tile() for x in self._tiles.values() if x.get_tile() is not None]
        return result

    def get_tiles_of_type(self, base_tile_type: Generic[T]) -> List[T]:
        result = [x for x in self._tiles.values() if isinstance(x, base_tile_type)]
        return result

    def get_tile_at_location(self, tileIndex: int) -> BaseTile:
        """Get the tile at the given location

        Returns: the tile. This may be null"""
        return self._tiles.get(tileIndex, None).get_tile()

    def get_effects(self) -> List[BaseEffect]:
        """Get a list of all the effects held by any tile in this container"""
        effects = map(lambda tile: tile.GetEffects(), self._tiles)
        effects = map(lambda tile: tile.GetEffects(), self.get_tiles())
        return list(effects)

    def get_effects_of_type(self, tile_type: Generic[T]) -> List[T]:
        """Get a list of all of the effects which extend a certain base effect in this container"""
        result = [x for x in self.get_effects() if isinstance(x, tile_type)]
        return result

    def place_tile(self, tile: BaseTile, location: int, direction: TileDirectionEnum = None) -> bool:
        """Place a tile in this container

        Input:
        """
        if tile is None:
            raise ValueError("base tile")
        if location < 0 or location > 47:
            raise ValueError("location must point to a valid position")
        if tile in self._twinTiles and direction is None:
            raise ValueError("direction cannot be null if tile is a twin tile")

        tile_type = TileTypeEnum.furnishedDwelling if tile.is_dwelling() else TileTypeEnum.furnishedCavern

        available_locations: List[int] = self.get_available_locations(tile_type)
        if location in available_locations:
            self._tiles[location].set_tile(tile)
            return True
        return False

    def get_available_locations(self, tile_type: TileTypeEnum) -> List[int]:
        """Get all locations available for a tile with the given type"""
        effects: Iterable[ChangeRequisiteEffect] = self.get_effects_of_type(ChangeRequisiteEffect)

        # gotta clone dictionary
        all_tile_requisites: Dict[TileTypeEnum, List[TileTypeEnum]] = dict(self._tileRequisites)

        for effect in effects:
            effect.invoke(all_tile_requisites)

        # get the correct requisites -- if adjacent, allow unavailable
        tile_requisites: List[TileTypeEnum] = all_tile_requisites[tile_type]

        # filter _tilesType by new requisites
        valid_positions: List[int] = [x[0] for x in self._tiles.items() if x[1].get_tile_type() in tile_requisites]

        # if twin, check all requisites for adjacent
        if tile_type not in self._twinTiles:
            return valid_positions

        valid_positions_with_adjacent: List[Tuple[int, TileDirectionEnum]] = []
        for position in valid_positions:
            adjacent_tile_locations: List[Tuple[int, TileDirectionEnum]] = self.get_adjacent_tiles(position)
            for adjacentTile in adjacent_tile_locations:
                adjacent_tile_type: TileTypeEnum = self._tiles[adjacentTile[0]].get_tile_type()
                if adjacent_tile_type in tile_requisites:
                    valid_positions_with_adjacent.append((position, adjacentTile[1]))
                    break

        return list(map(
            lambda valid_position_with_adjacent: valid_position_with_adjacent[0], valid_positions_with_adjacent))
        # only unavailable with adjacent (in correct section) will pass both checks

    def get_adjacent_tiles(self, location: int) -> List[Tuple[int, TileDirectionEnum]]:
        if location < 0 or location > self._tileCount:
            raise ValueError

        direction_offset = {
            TileDirectionEnum.up: -8,
            TileDirectionEnum.down: 8,
            TileDirectionEnum.left: -1,
            TileDirectionEnum.right: 1}

        adjacent_direction_condition = {
            TileDirectionEnum.up: lambda adjloc: adjloc > 0,
            TileDirectionEnum.down: lambda adjloc: adjloc < self._tileCount,
            TileDirectionEnum.left: lambda adjloc: adjloc % self._width != 7,
            TileDirectionEnum.right: lambda adjloc: adjloc % self._width != 0}

        result = []

        for x in direction_offset:
            adjacent_location = location + direction_offset[x]
            if adjacent_direction_condition[x](adjacent_location):
                result.append((adjacent_location, x))

        return result
