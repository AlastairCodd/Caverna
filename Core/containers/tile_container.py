from typing import List, Tuple, Dict
from common.entities.tile_entity import TileEntity
from core.enums.caverna_enums import TileDirectionEnum, TileTypeEnum
from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile
from buisness_logic.effects import board_effects
from common.defaults import tile_container_default, tile_twin_default, tile_requisite_default


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

    def get_tiles(self) -> List[BaseTile]:
        """Get the base tiles contained in this container"""
        result = [x.get_tile() for x in self._tiles.values() if x.get_tile() is not None]
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

    def get_effects_of_type(self, tileType) -> List[BaseEffect]:
        """Get a list of all of the effects which extend a certain base effect in this container"""
        result = [x for x in self.get_effects() if isinstance(x, tileType)]
        return result

    def place_tile(self, tile: BaseTile, location: int, direction: TileDirectionEnum = None) -> bool:
        """Place a tile in this container

        Input:
        """
        if tile is None:
            raise ValueError("base tile")

        if location < 0 or location > 47:
            raise ValueError("base tile")

        if tile in self._twinTiles and direction is None:
            raise ValueError("direct cannot be null if tile is a twin tile")

        available_locations = self.get_available_locations(tile)
        if location in available_locations:
            self._tiles.append(tile)

    def get_available_locations(self, tile: TileTypeEnum) -> List[int]:
        effects = self.get_effects_of_type(board_effects.BaseBoardEffect)

        # gotta clone dictionary
        allTileRequisites = dict(self._tileRequisites)

        for effect in effects:
            effect.invoke(allTileRequisites)

        # get the correct requisites -- if adjacent, allow unavailable
        tileRequisites: List[TileTypeEnum] = allTileRequisites[tile]

        # filter _tilesType by new requisites
        validPositions: List[int] = [x for x in self._tilesType if self._tilesType[x] in tileRequisites]

        # if twin, check all requisites for adjacent
        if tile not in self._twinTiles:
            return validPositions

        valid_positions_with_adjacent: List[Tuple[int, TileDirectionEnum]] = []
        for position in validPositions:
            adjacent_tiles: List[Tuple[int, TileDirectionEnum]] = self.GetAdjacentTiles(position)
            for adjacentTile in adjacent_tiles:
                if self._tilesType[adjacentTile[0]] in tileRequisites:
                    valid_positions_with_adjacent.append((position, adjacentTile[1]))
                    break
        return list(map(lambda valid_position_with_adjacent: valid_position_with_adjacent[0], valid_positions_with_adjacent))
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
