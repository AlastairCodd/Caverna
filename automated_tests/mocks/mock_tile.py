from typing import List, Dict

from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import TileColourEnum, ResourceTypeEnum


class MockTile(BaseTile):
    def __init__(
            self,
            name: str = "Mock",
            tile_id: int = 0,
            is_dwelling: bool = False,
            base_points: int = 0,
            cost: Dict[ResourceTypeEnum, int] = [],
            effects: List[BaseEffect] = [],
            colour: TileColourEnum = TileColourEnum.Green):
        super().__init__(name, tile_id, is_dwelling, base_points, cost, effects, colour)