from common.entities.dwarf import Dwarf
from common.entities.player import Player
from core.baseClasses.base_action import BaseAction
from core.containers.resource_container import ResourceContainer
from core.enums.caverna_enums import TileTypeEnum


class PlaceATileAction(BaseAction):
    def __init__(self, tile_type: TileTypeEnum):
        self._tileType = tile_type

    def invoke(self, player: Player, active_card: ResourceContainer, current_dwarf: Dwarf) -> bool:
        raise NotImplementedError

    def new_turn_reset(self):
        pass
