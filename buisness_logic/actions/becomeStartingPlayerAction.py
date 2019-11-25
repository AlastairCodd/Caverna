from typing import Union

from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from common.entities.player import Player
from core.baseClasses.base_card import BaseCard


class BecomeStartingPlayerAction(BaseAction):
    def __init__(self):
        self._starting_player_next_turn: Union[Player, None] = None

    def invoke(self, player: Player, active_card: BaseCard, current_dwarf: Dwarf) -> ResultLookup[int]:
        """Sets a flag which results in the current player becoming the starting player at the start of the next turn.
        The play order continues as normal.

        :param player: The player who is now the starting player.
        :param active_card: Unused.
        :param current_dwarf: Unused.
        :return: True if the
        """
        if player is None:
            raise ValueError("player")

        result: ResultLookup[int]
        if self._starting_player_next_turn is None:
            self._starting_player_next_turn = player
            result = ResultLookup(True, 1)
        else:
            result = ResultLookup(False, 0, f"Someone else (player {self._starting_player_next_turn.id}) is already starting player next turn")

        return result

    def new_turn_reset(self):
        self._starting_player_next_turn = None
