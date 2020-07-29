from collections import namedtuple
from typing import List, Dict

from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository

DwarvesByLevel = namedtuple("DwarvesByLevel", 'dwarves lowest_level')


class AvailableDwarfService(object):
    def can_player_use_a_dwarf_out_of_order(
            self,
            player: BasePlayerRepository) -> ResultLookup[bool]:
        if player is None:
            raise ValueError("Player may not be null")

        errors: List[str] = []

        if player.get_resources_of_type(ResourceTypeEnum.ruby) < 1:
            errors.append("Insufficient resources to use a dwarf out of order.")

        dwarves_by_level: DwarvesByLevel = self.get_available_dwarves_by_level(player)
        does_player_have_available_dwarves_of_multiple_levels: bool = len(dwarves_by_level.dwarves) > 1
        if not does_player_have_available_dwarves_of_multiple_levels:
            errors.append("No dwarves of different level to default")

        success: bool = len(errors) == 0
        result: ResultLookup[bool] = ResultLookup(success, success, errors)
        return result

    def get_available_dwarves_by_level(self, player: BasePlayerRepository) -> DwarvesByLevel:
        if player is None:
            raise ValueError("Player cannot be none")

        available_dwarves: List[Dwarf] = [dwarf for dwarf in player.dwarves if not dwarf.is_active and dwarf.is_adult]

        if len(available_dwarves) == 0:
            raise IndexError("Player must have at least one dwarf available")

        lowest_level_of_dwarves: int = 100
        available_dwarves_by_level: Dict[int, List[Dwarf]] = {}
        for dwarf in available_dwarves:
            if dwarf.weapon_level in available_dwarves_by_level:
                available_dwarves_by_level[dwarf.weapon_level].append(dwarf)
            else:
                available_dwarves_by_level[dwarf.weapon_level] = [dwarf]

            if dwarf.weapon_level < lowest_level_of_dwarves:
                lowest_level_of_dwarves = dwarf.weapon_level

        result: DwarvesByLevel = DwarvesByLevel(available_dwarves_by_level, lowest_level_of_dwarves)
        return result
