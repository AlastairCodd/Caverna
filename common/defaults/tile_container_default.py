from typing import Dict, List

from buisness_logic.tiles.dwelling import EntryLevelDwelling
from buisness_logic.tiles.mine_tiles import CavernTile
from buisness_logic.tiles.transparent_tile import TransparentTile
from common.entities.tile_entity import TileEntity
from core.baseClasses.base_tile_container_default import BaseTileContainerDefault
from core.constants import game_constants
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum


class TileContainerDefault(BaseTileContainerDefault):
    def __init__(self) -> None:
        self._last_row_index: int = game_constants.default_board_tile_count - game_constants.default_board_width
        self._first_column_index: int = 0
        self._last_column_index: int = game_constants.default_board_width - 1

    def assign(
            self,
            tile_collection: Dict[int, TileEntity]) -> Dict[int, TileEntity]:
        """Fills the given dictionary with the default tile layout"""
        if tile_collection is None:
            raise ValueError("currentTiles")

        tile_collection.clear()

        tiles_types: List[TileTypeEnum] = []

        for tile_id in range(game_constants.default_board_tile_count):
            tile_type: TileTypeEnum
            column_id: int = tile_id % game_constants.default_board_width
            if tile_id < game_constants.default_board_width \
                    or tile_id > self._last_row_index \
                    or column_id == self._first_column_index \
                    or column_id == self._last_column_index:
                tile_type = TileTypeEnum.unavailable
            elif column_id < 4:
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

        tiles[11].set_tile(TransparentTile(tiles[11], ResourceTypeEnum.boar))
        tiles[25].set_tile(TransparentTile(tiles[25], ResourceTypeEnum.boar))
        tiles[34].set_tile(TransparentTile(tiles[34], ResourceTypeEnum.food))

        tiles[14].set_tile(TransparentTile(tiles[14], ResourceTypeEnum.food, 2))
        tiles[37].set_tile(TransparentTile(tiles[37], ResourceTypeEnum.food))

        # make overhanging tiles give coins
        for (location, tile) in tiles.items():
            if tile.tile_type != TileTypeEnum.unavailable:
                continue
            tiles[location].set_tile(TransparentTile(tiles[location], ResourceTypeEnum.coin, 2))

        return tiles
