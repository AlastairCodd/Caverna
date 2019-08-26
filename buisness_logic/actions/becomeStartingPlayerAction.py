from typing import Union

from common.entities.dwarf import Dwarf
from core.baseClasses.base_action import BaseAction
from common.entities.player import Player
from core.containers.resource_container import ResourceContainer


class BecomeStartingPlayerAction(BaseAction):
    def __init__(self):
        self._starting_player_next_turn: Union[Player, None] = None

    def invoke(self, player: Player, active_card: ResourceContainer, current_dwarf: Dwarf) -> bool:
        """Sets a flag which results in the current player becoming the starting player at the start of the next turn.
        The play order continues as normal.

        :param player: The player who is now the starting player.
        :param active_card: Unused.
        :param current_dwarf: Unused.
        :return: True if the
        """
        if player is None:
            raise ValueError("player")

        result: bool
        if self._starting_player_next_turn is None:
            self._starting_player_next_turn = player
            result = True
        else:
            result = False

        return result

    def new_turn_reset(self):
        self._starting_player_next_turn = None
