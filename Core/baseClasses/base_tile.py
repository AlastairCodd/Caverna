from typing import Dict, List
from core.enums.caverna_enums import ResourceTypeEnum
from core.baseClasses.base_effect import BaseEffect


class BaseTile(object):

    def __init__(
            self,
            name: str,
            tile_id: int,
            is_dwelling: bool = False,
            base_points: int = 0,
            cost: Dict[ResourceTypeEnum, int] = {},
            effects: List[BaseEffect] = []):
        """Constructor for base Tile class. """
        self._name = name
        self._id = tile_id
        self._isDwelling = is_dwelling
        self._basePoints = base_points
        self._cost = cost
        self._effects = effects
