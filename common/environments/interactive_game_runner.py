from common.environments.caverna_env import CavernaEnv


class InteractiveGameRunner(object):
    def __init__(
            self,
            number_of_players: int) -> None:
        self._caverna_env: CavernaEnv = CavernaEnv(number_of_players)

    def run(self) -> None:
        self._caverna_env.reset()

        has_game_finished: bool = False

        while not has_game_finished:
            unused_array, reward, has_game_finished, unused_info = self._caverna_env.step()
