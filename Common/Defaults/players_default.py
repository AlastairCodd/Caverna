from typing import List

from core.enums.caverna_enums import ResourceTypeEnum
from core.services.base_player_service import BasePlayerService


class PlayersDefault(object):
    def __init__(
            self,
            number_of_players: int = 7):
        self._initialFood = [1, 1, 2, 3, 3, 3, 3]

        if number_of_players < 1:
            raise IndexError(f"Must have at least one player (number_of_players={number_of_players})")
        if number_of_players > 7:
            raise IndexError(f"The maximum number of players is {len(self._initialFood)} (number_of_players={number_of_players})")
        self._numberOfPlayers = number_of_players

    def assign(self, players: List[BasePlayerService]) -> List[BasePlayerService]:
        if players is None:
            raise ValueError("playersList")
        players.clear()

        for x in range(self._numberOfPlayers):
            new_player = BasePlayerService(x, x)
            new_player.give_resource(ResourceTypeEnum.food, self._initialFood[x])
            players.append(new_player)

        return players
