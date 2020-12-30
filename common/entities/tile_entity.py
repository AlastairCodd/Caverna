from typing import List, Optional, Generic, TypeVar

from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile, BaseSpecificTile
from core.enums.caverna_enums import TileTypeEnum, ResourceTypeEnum, TileColourEnum

T = TypeVar('T')


class TileEntity(object):
    def __init__(
            self,
            tile_id: int,
            tile_type: TileTypeEnum,
            base_tile: Optional[BaseTile] = None,
            has_stable: bool = False):
        self._id = tile_id
        self._tile_type: TileTypeEnum = tile_type
        self._specific_tile: Optional[BaseTile] = base_tile

        self._has_stable: bool = has_stable

    @property
    def id(self):
        return self._id

    @property
    def tile(self) -> Optional[BaseTile]:
        return self._specific_tile

    @property
    def has_effects(self) -> bool:
        result: bool
        if self._specific_tile is None:
            result = False
        else:
            result = len(self._specific_tile.effects) > 0
        return result

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

    @property
    def has_stable(self) -> bool:
        return self._has_stable

    def get_effects_of_type(
            self,
            effect_type: Generic[T]) -> List[T]:
        """Get a list of all of the effects which extend a certain base effect"""
        if effect_type is None:
            raise ValueError("Effect Type may not be none")
        result: List[T]
        if self._specific_tile is None or len(self._specific_tile.effects) == 0:
            result = []
        else:
            result = [effect for effect in self._specific_tile.effects if isinstance(effect, effect_type)]
        return result

    def set_tile(
            self,
            base_tile: BaseTile) -> None:
        # if self._specific_tile is not None:
        #     raise ValueError("Cannot set specific tile; already has a tile")
        self._specific_tile = base_tile
        self._tile_type = base_tile.tile_type

    def give_stable(self) -> bool:
        result: bool = False
        if not self._has_stable:
            self._has_stable = True
            result = True

        return result
