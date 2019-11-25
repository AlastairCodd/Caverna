from typing import List

from common.entities.dwarf import Dwarf
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard


class UpgradeAllWeaponsAction(BaseAction):
    def invoke(self, player: Player, active_card: BaseCard, current_dwarf: Dwarf) -> ResultLookup[int]:
        """Increases the level of all weapons owned by dwarves.

        :param player: The player who has dwarves. This may not be null.
        :param active_card: Unused.
        :param current_dwarf: Unused.
        :return: False if no dwarves can have weapons upgraded, true otherwise.
        """
        if player is None:
            raise ValueError(str(player))
        successes: int = 0
        errors: List[str] = []

        for dwarf in player.dwarves:
            if dwarf.has_weapon:
                increase_level_result: ResultLookup[int] = dwarf.weapon.increase_level()
                if increase_level_result.flag:
                    successes += 1
                else:
                    for error in increase_level_result.errors:
                        errors.append(error)

        result: ResultLookup[int] = ResultLookup(successes > 0, successes, errors)
        return result

    def new_turn_reset(self):
        pass
