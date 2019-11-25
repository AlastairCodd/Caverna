from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.enums.caverna_enums import TileTypeEnum


class PlaceATileAction(BaseAction):
    def __init__(self, tile_type: TileTypeEnum):
        self._tileType = tile_type

    def invoke(self, player: Player, active_card: BaseCard, current_dwarf: Dwarf) -> ResultLookup[int]:
        raise NotImplementedError

    def new_turn_reset(self):
        pass
