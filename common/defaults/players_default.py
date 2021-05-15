from typing import List

from buisness_logic.services.player_services.keyboard_human_player_service import KeyboardHumanPlayerService
from core.enums.caverna_enums import ResourceTypeEnum
from core.services.base_player_service import BasePlayerService


class PlayersDefault(object):
    def __init__(
            self,
            number_of_players: int = 7):
        self._initial_food: List[int] = [1, 1, 2, 3, 3, 3, 3]
        self._names: List[str] = ["Kaite", "Inth", "Callie", "Merra", "Tali", "Menxing", "Belville"]

        if number_of_players < 1:
            raise IndexError(f"Must have at least one player (number_of_players={number_of_players})")
        if number_of_players > 7:
            raise IndexError(f"The maximum number of players is {len(self._initial_food)} (number_of_players={number_of_players})")
        self._number_of_players = number_of_players

    def assign(self, players: List[BasePlayerService]) -> List[BasePlayerService]:
        if players is None:
            raise ValueError("Players cannot be None")
        players.clear()

        for x in range(self._number_of_players):
            new_player: BasePlayerService = KeyboardHumanPlayerService(x, self._names[x], x)
            new_player.give_resource(ResourceTypeEnum.food, self._initial_food[x])
            players.append(new_player)

        return players
