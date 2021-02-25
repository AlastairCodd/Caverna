from common.environments.caverna_env import CavernaEnv


class InteractiveGameRunner(object):
    def __init__(self) -> None:
        self._caverna_env: CavernaEnv = CavernaEnv()

    def run(self) -> None:
        self._caverna_env.reset()

        has_game_finished: bool = False

        while not has_game_finished:
            unused_array, reward, has_game_finished, unused_info = self._caverna_env.step()
