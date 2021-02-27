from typing import Optional

from common.defaults.tile_container_default import TileContainerDefault
from core.baseClasses.base_tile_container_default import BaseTileContainerDefault
from core.repositories.base_player_repository import BasePlayerRepository


class SimplePlayerRepository(BasePlayerRepository):
    """For use with the PlayerPrototype, when running ordering of actions."""
    def __init__(
            self,
            player_id: int,
            turn_index: int,
            tile_container_default: Optional[BaseTileContainerDefault] = None) -> None:
        tile_container_default = TileContainerDefault() if tile_container_default is None else tile_container_default
        BasePlayerRepository.__init__(self, player_id, turn_index, tile_container_default)
