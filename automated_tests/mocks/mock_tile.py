from typing import List, Dict, Optional

from core.baseClasses.base_effect import BaseEffect
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum


class MockTile(BaseTile):
    def __init__(
            self,
            name: str = "Mock",
            tile_id: int = 0,
            tile_type: TileTypeEnum = TileTypeEnum.furnishedCavern,
            base_points: int = 0,
            cost: Optional[Dict[ResourceTypeEnum, int]] = None,
            effects: Optional[List[BaseEffect]] = None):
        BaseTile.__init__(
            self,
            name,
            tile_id,
            tile_type,
            base_points,
            cost,
            effects)