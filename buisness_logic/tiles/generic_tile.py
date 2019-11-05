from typing import Dict, List

from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum, TileColourEnum


class GenericTile(BaseTile):
    def __init__(
            self,
            name: str,
            tile_id: int,
            is_dwelling: bool,
            base_points: int,
            cost: Dict[ResourceTypeEnum, int],
            effects: List[BaseEffect],
            colour: TileColourEnum):
        BaseTile.__init__(
            self,
            name,
            tile_id,
            is_dwelling,
            base_points,
            cost,
            effects,
            colour)
