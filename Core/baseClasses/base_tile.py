from typing import Dict, List
from core.enums.caverna_enums import ResourceTypeEnum, TileColourEnum
from core.baseClasses.base_effect import BaseEffect


class BaseTile(object):

    def __init__(
            self,
            name: str,
            tile_id: int,
            is_dwelling: bool = False,
            base_points: int = 0,
            cost: Dict[ResourceTypeEnum, int] = None,
            effects: List[BaseEffect] = None,
            colour: TileColourEnum = TileColourEnum.Green):
        """Constructor for base Tile class.
        :param name: The name of the tile. This cannot be null.
        :param tile_id: The unique id of the tile.
        :param is_dwelling: A flag determining if the tile is a dwelling tile.
        :param cost: The unaltered cost of purchasing the tile. This cannot be null.
        :param effects: The effects which the tile causes. This cannot be null.
        :param colour: The colour of the tile.
        """
        if name is None or name.isspace():
            raise ValueError("tile name cannot be null or whitespace")
        self._name: str = name
        self._id: int = tile_id
        self._isDwelling: bool = is_dwelling
        self._basePoints: int = base_points

        if cost is None:
            cost = {}
        self._cost: Dict[ResourceTypeEnum, int] = cost

        if effects is None:
            effects = []
        self._effects: List[BaseEffect] = effects
        self._location: int = -1
        self._color: TileColourEnum = colour

    @property
    def is_dwelling(self) -> bool:
        return self.is_dwelling

    @property
    def base_points(self) -> int:
        return self._basePoints

    @property
    def location(self) -> int:
        return self._location

    @property
    def colour(self) -> TileColourEnum:
        return TileColourEnum