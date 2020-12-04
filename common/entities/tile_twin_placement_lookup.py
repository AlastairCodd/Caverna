from typing import NamedTuple

from core.enums.caverna_enums import TileDirectionEnum


class TileTwinPlacementLookup(NamedTuple):
    location: int
    direction: TileDirectionEnum
