from typing import List, Optional, Generic, TypeVar, Callable

from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile, BaseSpecificTile
from core.enums.caverna_enums import TileTypeEnum, TileColourEnum

T = TypeVar('T')


class TileEntity(object):
    def __init__(
            self,
            tile_id: int,
            tile_type: TileTypeEnum,
            on_change_callback: Optional[Callable[[int, BaseTile], None]]):
        self._id = tile_id
        self._tile_type: TileTypeEnum = tile_type
        self._specific_tile: Optional[BaseTile] = None
        self._has_effects = False

        self._has_stable: bool = False
        self._on_change_callback = on_change_callback

    @property
    def id(self):
        return self._id

    @property
    def tile(self) -> Optional[BaseTile]:
        return self._specific_tile

    @property
    def has_effects(self) -> bool:
        return self._has_effects

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

    @property
    def points(self) -> int:
        return self._specific_tile.base_points if self._specific_tile is not None else 0

    def get_effects_of_type(
            self,
            effect_type: Generic[T]) -> List[T]:
        """Get a list of all of the effects which extend a certain base effect"""
        if effect_type is None:
            raise ValueError("Effect Type may not be none")
        if not self._has_effects:
            return []
        return [effect for effect in self._specific_tile.effects if isinstance(effect, effect_type)]

    def set_tile(
            self,
            base_tile: BaseTile) -> None:
        # if self._specific_tile is not None:
        #     raise ValueError("Cannot set specific tile; already has a tile")
        self._specific_tile = base_tile
        self._tile_type = base_tile.tile_type
        self._has_effects = len(self._specific_tile.effects) > 0

        if self._on_change_callback is not None:
            self._on_change_callback(self._id, self._specific_tile)

    def give_stable(self) -> bool:
        result: bool = False
        if not self._has_stable:
            self._has_stable = True
            result = True

        return result
