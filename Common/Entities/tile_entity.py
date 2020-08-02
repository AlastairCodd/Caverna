from typing import List, Optional

from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile, BaseSpecificTile
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum, TileColourEnum


class TileEntity(object):
    def __init__(
            self,
            tile_id: int,
            tile_type: TileTypeEnum,
            base_tile: Optional[BaseTile] = None,
            animal_type: Optional[ResourceTypeEnum] = None,
            animal_quantity: int = 0,
            has_stable: bool = False):
        self._id = tile_id
        self._tile_type: TileTypeEnum = tile_type
        self._specific_tile: Optional[BaseTile] = base_tile
        self._animalType: Optional[ResourceTypeEnum] = animal_type
        self._animalQuantity: int = animal_quantity
        self._hasStable: bool = has_stable

    @property
    def tile(self) -> Optional[BaseTile]:
        return self._specific_tile

    @property
    def effects(self) -> List[BaseEffect]:
        result: List[BaseEffect]
        if self._specific_tile is not None:
            result = self._specific_tile.effects
        else:
            result = []
        return result

    @property
    def colour(self) -> Optional[TileColourEnum]:
        result: Optional[TileColourEnum] = None
        if self._specific_tile is not None and isinstance(self._specific_tile, BaseSpecificTile):
            result = self._specific_tile.colour
        return result

    @property
    def tile_type(self) -> TileTypeEnum:
        return self._tile_type

    def set_tile(
            self,
            base_tile: BaseTile):
        if self._specific_tile is not None:
            raise ValueError("Cannot set specific tile; already has a tile")
        self._specific_tile = base_tile
