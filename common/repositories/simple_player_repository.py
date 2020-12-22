from typing import Dict

from common.entities.tile_entity import TileEntity
from core.baseClasses.base_tile_container_default import BaseTileContainerDefault
from core.repositories.base_player_repository import BasePlayerRepository


class SimplePlayerRepository(BasePlayerRepository):
    def __init__(
            self,
            player_id: int,
            turn_index: int) -> None:
        BasePlayerRepository.__init__(self, player_id, turn_index, NullTileContainerDefault())


class NullTileContainerDefault(BaseTileContainerDefault):
    def assign(
            self,
            tile_collection: Dict[int, TileEntity]) -> Dict[int, TileEntity]:
        return {}