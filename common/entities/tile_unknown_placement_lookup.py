from typing import NamedTuple, Optional

from core.enums.caverna_enums import TileDirectionEnum


class TileUnknownPlacementLookup(NamedTuple):
    location: int
    direction: Optional[TileDirectionEnum]
