from typing import Optional

from common.environments.caverna_env import CavernaEnv


class InteractiveGameRunner(object):
    def __init__(
            self,
            number_of_players: Optional[int],
            player_default = None) -> None:
        self._caverna_env: CavernaEnv = CavernaEnv(players_default=player_default) \
                if number_of_players is None \
                else CavernaEnv(number_of_players=number_of_players, players_default=player_default)

    def run(self) -> None:
        self._caverna_env.reset()

        has_game_finished: bool = False

        while not has_game_finished:
            unused_array, reward, has_game_finished, unused_info = self._caverna_env.step()
