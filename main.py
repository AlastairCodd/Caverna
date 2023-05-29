from typing import Dict, Any
import logging

from InquirerPy.utils import color_print
from InquirerPy import inquirer

from common.environments.interactive_game_runner import InteractiveGameRunner
from core.constants.logging import VERBOSE_LOG_LEVEL


def _configure_logging():
    logging.basicConfig(
            format='[%(levelname)s] %(message)s',
            level=VERBOSE_LOG_LEVEL)
    logging.addLevelName(logging.CRITICAL, "FTL")
    logging.addLevelName(logging.ERROR, "ERR")
    logging.addLevelName(logging.WARNING, "WRN")
    logging.addLevelName(logging.INFO, "INF")
    logging.addLevelName(logging.DEBUG, "DBG")
    logging.addLevelName(VERBOSE_LOG_LEVEL, "VRB")
    logging.getLogger('asyncio').setLevel(logging.WARN)


if __name__ == "__main__":
    _configure_logging()

    color_print(
        formatted_text=[("", "Welcome to...\r\n"), ("class:emphasis", "Cavernabot!"), ("","\r\n")],
        style={"emphasis": "fg:yellow bold"},
    )

    number_of_players = int(inquirer.number(
        message="How many players are playing?",
        min_allowed=2,
        max_allowed=7
    ).execute())

    print()

    game_runner: InteractiveGameRunner = InteractiveGameRunner(number_of_players)
    game_runner.run()
