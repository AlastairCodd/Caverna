from buisness_logic.services.player_services.action_choice_player_service import ActionChoicePlayerService
from core.enums.caverna_enums import ResourceTypeEnum


class ActionChoicePlayersDefault():
    def __init__(self, number_of_players: int = 7):
        self._initial_food: list[int] = [1, 1, 2, 3, 3, 3, 3]
        self._names: list[str] = ["Robot Inth", "Robot Callie", "Robot Merra", "Robot Tali", "Robot Menxing", "Robot Kaite", "Robot Belville"]

        if number_of_players < 1:
            raise IndexError(f"Must have at least one player (number_of_players={number_of_players})")
        if number_of_players > 7:
            raise IndexError(f"The maximum number of players is {len(self._initial_food)} (number_of_players={number_of_players})")
        self._number_of_players = number_of_players

    def assign(self, players):
        if players is None:
            raise ValueError()
        players.clear()

        for x in range(self._number_of_players):
            new_player = ActionChoicePlayerService(x, self._names[x], x)
            new_player.give_resource(ResourceTypeEnum.food, self._initial_food[x])
            players.append(new_player)

        return players
