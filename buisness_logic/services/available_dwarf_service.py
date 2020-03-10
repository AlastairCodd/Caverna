from typing import List

from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup


class AvailableDwarfService(object):
    def can_player_use_a_dwarf_out_of_order(self, player: Player) -> ResultLookup[bool]:
        if player is None:
            raise ValueError
        result: ResultLookup[bool] = ResultLookup(errors="No dwarves of different level to default")
        return result

    def get_available_dwarves(
            self,
            player: Player,
            is_using_a_dwarf_out_of_order: bool) -> List[Dwarf]:
        if player is None:
            raise ValueError
        result: List[Dwarf] = []
        return result
