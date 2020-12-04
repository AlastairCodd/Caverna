from typing import Dict, List

from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile, BaseSpecificTile
from core.enums.caverna_enums import ResourceTypeEnum, TileColourEnum, TileTypeEnum


class GenericTile(BaseTile):
    def __init__(
            self,
            name: str,
            tile_id: int,
            tile_type: TileTypeEnum,
            base_points: int,
            cost: Dict[ResourceTypeEnum, int],
            effects: List[BaseEffect]):
        BaseTile.__init__(
            self,
            name,
            tile_id,
            tile_type,
            base_points,
            cost,
            effects)


class GenericSpecificTile(BaseSpecificTile):
    def __init__(
            self,
            name: str,
            tile_id: int,
            tile_type: TileTypeEnum,
            base_points: int,
            cost: Dict[ResourceTypeEnum, int],
            effects: List[BaseEffect],
            colour: TileColourEnum):
        BaseSpecificTile.__init__(
            self,
            name,
            tile_id,
            tile_type,
            base_points,
            cost,
            effects,
            colour)
