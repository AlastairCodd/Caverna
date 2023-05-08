from typing import List, Dict, TypeVar, Generic, cast, Optional

from common.entities.tile_entity import TileEntity
from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile
from core.baseClasses.base_tile_container_default import BaseTileContainerDefault
from core.constants import game_constants
from core.enums.caverna_enums import TileTypeEnum

T = TypeVar('T')


class TileContainer(object):
    def __init__(
            self,
            tile_container_default: BaseTileContainerDefault,
            height: int = game_constants.default_board_height,
            width: int = game_constants.default_board_width):
        if tile_container_default is None:
            raise ValueError("Tile Container Default cannot be null")
        if height < 0:
            raise ValueError("height must be greater than 0")
        if width < 0:
            raise ValueError("width must be greater than 0")
        self._height: int = height
        self._width: int = width

        self._tile_count: int = height * width

        self._tiles: Dict[int, TileEntity] = {}

        self._cached_effects: Dict[T, List[T]] = {}
        tile_container_default.set_on_tile_changed_callback(self._on_tile_changed_callback)
        tile_container_default.assign(self._tiles)

    def get_number_of_tiles_of_type(self, tile_type: TileTypeEnum) -> int:
        # i hate python
        return sum(1 for t in self._tiles.values() if t.tile_type == tile_type)

    @property
    def tile_count(self) -> int:
        return self._tile_count

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def tiles(self) -> Dict[int, TileEntity]:
        """Get the tiles contained in this container"""
        return self._tiles

    def get_tile_at_location(self, tile_index: int) -> TileEntity:
        if tile_index < 0 or tile_index >= self._tile_count:
            raise IndexError(f"Tile Index ({tile_index}) must be in range [0, Number of Tiles: {self._tile_count})")
        return self._tiles[tile_index]

    def get_tiles_of_type(
            self,
            base_tile_type: Generic[T]) -> List[T]:
        """Get the (base tiles) tiles which extend some base type."""
        result = [cast(base_tile_type, x.tile) for x in self._tiles.values() if isinstance(x.tile, base_tile_type)]
        return result

    def get_specific_tile_at_location(
            self,
            tile_index: int) -> Optional[BaseTile]:
        """Get the tile at the given location

        :param tile_index: The location to get the tile for. This must be in the range [0, self._tileCount).
        :return: The base tile at the given location, if it exists. If there is no tile, the result will be none."""
        if tile_index < 0 or tile_index > self._tile_count:
            raise ValueError()
        return self._tiles.get(tile_index, None).tile

    @property
    def effects(self) -> List[BaseEffect]:
        """Get a list of all the effects held by any tile in this container"""
        effects = [effect for tile in self._tiles.values() for effect in tile.effects]
        return effects

    def get_effects_of_type(
            self,
            effect_type: Generic[T]) -> List[T]:
        """Get a list of all of the effects which extend a certain base effect in this container"""
        if effect_type is None:
            raise ValueError("Effect Type may not be none")
        if effect_type in self._cached_effects:
            return self._cached_effects[effect_type]
        result = [effect for tile in self._tiles.values() if tile.has_effects for effect in tile.effects if isinstance(effect, effect_type)]
        self._cached_effects[effect_type] = result
        return result

    def _on_tile_changed_callback(self, tile_id: int, tile) -> None:
        self._cached_effects.clear()
