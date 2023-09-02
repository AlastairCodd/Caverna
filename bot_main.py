from typing import Dict, Any
import logging

from common.environments.interactive_game_runner import InteractiveGameRunner
from core.constants.logging import VERBOSE_LOG_LEVEL
from common.defaults.action_choice_players_default import ActionChoicePlayersDefault


def _configure_logging():
    logging.basicConfig(
            format='[%(levelname)s] %(message)s',
            filename="bot_players_logging",
            filemode="w",
            level=VERBOSE_LOG_LEVEL)

    logging.addLevelName(logging.CRITICAL, "FTL")
    logging.addLevelName(logging.ERROR, "ERR")
    logging.addLevelName(logging.WARNING, "WRN")
    logging.addLevelName(logging.INFO, "INF")
    logging.addLevelName(logging.DEBUG, "DBG")
    logging.addLevelName(VERBOSE_LOG_LEVEL, "VRB")
    
    logging.getLogger('asyncio').setLevel(logging.WARN)
    logging.getLogger('').addHandler(logging.StreamHandler())


if __name__ == "__main__":
    _configure_logging()

    print("d[o_0]b Cavernabot initialising...\r\n")

    game_runner: InteractiveGameRunner = InteractiveGameRunner(3, ActionChoicePlayersDefault())
    try:
        game_runner.run()
    except:
        logging.exception('')
        raise
