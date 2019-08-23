from typing import Dict, List
from core.enums.caverna_enums import TileTypeEnum
from common.entities.tile_entity import TileEntity


class TileContainerDefault(object):

    def assign(
            self,
            currentTiles: Dict[int, TileEntity]) -> Dict[int, TileEntity]:
        """Fills the given dictionary with the default tile layout"""
        if currentTiles is None:
            raise ValueError("currentTiles")

        currentTiles.clear()

        tiles_types: List[TileTypeEnum] = []

        for tile_id in range(48):
            tile_type: TileTypeEnum
            if tile_id < 8 or tile_id > 40 or tile_id % 8 == 0 or tile_id % 8 == 7:
                tile_type = TileTypeEnum.unavailable
            elif tile_id % 8 < 4:
                tile_type = TileTypeEnum.forest
            else:
                tile_type = TileTypeEnum.underground

            tiles_types.append(tile_type)

        overridden_tiles_types = self._specificIntialTileOverrides(tiles_types)

        tiles = {tile_id: TileEntity(tile_id, overridden_tiles_types[tile_id])
                 for tile_id in range(len(overridden_tiles_types))}
        currentTiles.update(tiles)

        return currentTiles

    def _specificIntialTileOverrides(
            self,
            current_tile_type: List[TileTypeEnum]) -> List[TileTypeEnum]:
        """Overrides specific current tiles

        currentTiles: a dictionary of int to TileTypeEnum. This cannot be null
        returns: currentTiles"""
        if current_tile_type is None:
            raise ValueError("currentTiles")
        current_tile_type[28] = TileTypeEnum.cavern
        current_tile_type[36] = TileTypeEnum.furnishedDwelling

        return current_tile_type
