from typing import Dict, List

from buisness_logic.tiles.dwelling import EntryLevelDwelling
from buisness_logic.tiles.mine_tiles import CavernTile
from core.baseClasses.base_tile_container_default import BaseTileContainerDefault
from core.enums.caverna_enums import TileTypeEnum
from common.entities.tile_entity import TileEntity


class TileContainerDefault(BaseTileContainerDefault):
    def assign(
            self,
            tile_collection: Dict[int, TileEntity]) -> Dict[int, TileEntity]:
        """Fills the given dictionary with the default tile layout"""
        if tile_collection is None:
            raise ValueError("currentTiles")

        tile_collection.clear()

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

        tiles: Dict[int, TileEntity] = {tile_id: TileEntity(tile_id, tiles_types[tile_id])
                                        for tile_id in range(len(tiles_types))}
        self._assign_specific_initial_tile_overrides(tiles)

        tile_collection.update(tiles)

        return tile_collection

    def _assign_specific_initial_tile_overrides(
            self,
            tiles: Dict[int, TileEntity]) -> Dict[int, TileEntity]:
        """Overrides specific current tiles

        :param tiles: A dictionary of int to tile entity. This cannot be null
        :returns: tiles. This will never be null."""
        if tiles is None:
            raise ValueError("empty_default_tiles may not be null")
        tiles[28].set_tile(CavernTile())
        tiles[36].set_tile(EntryLevelDwelling())

        return tiles
