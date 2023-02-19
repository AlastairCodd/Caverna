from typing import Dict, Any

from InquirerPy.utils import color_print
from InquirerPy import prompt

from buisness_logic.services.player_services.keyboard_human_player_service import create_question, QuestionTypeEnum
from common.environments.interactive_game_runner import InteractiveGameRunner

if __name__ == "__main__":
    color_print(
        formatted_text=[("", "Welcome to...\r\n"), ("class:emphasis", "Cavernabot!"), ("","\r\n")],
        style={"emphasis": "fg:yellow bold"},
    )

    def validate_number_of_players(chosen_number_of_players) -> bool:
        if not chosen_number_of_players.isdigit():
            return false
        return 2 <= int(chosen_number_of_players) <= 7

    name = "how_many_players"
    question: Dict[str, Any] = create_question(
        QuestionTypeEnum.input,
        name,
        "How many players are playing?",
        validator=validate_number_of_players
    )

    answer = prompt(question)
    number_of_players = int(answer[name])

    print()

    game_runner: InteractiveGameRunner = InteractiveGameRunner(number_of_players)
    game_runner.run()
