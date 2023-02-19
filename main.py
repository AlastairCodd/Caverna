from typing import Dict, Any

from InquirerPy.utils import color_print
from InquirerPy import inquirer

from common.environments.interactive_game_runner import InteractiveGameRunner

if __name__ == "__main__":
    color_print(
        formatted_text=[("", "Welcome to...\r\n"), ("class:emphasis", "Cavernabot!"), ("","\r\n")],
        style={"emphasis": "fg:yellow bold"},
    )

    number_of_players = int(inquirer.number(
        message="How many players are playing?",
        min_allowed=2,
        max_allowed=7,
        default=None,
    ).execute())

    print()

    game_runner: InteractiveGameRunner = InteractiveGameRunner(number_of_players)
    game_runner.run()
