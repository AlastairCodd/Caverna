import argh

from common.environments.interactive_game_runner import InteractiveGameRunner


@argh.arg('number_of_players', choices=list(range(2,8)))
def main(number_of_players: int) -> None:
    game_runner: InteractiveGameRunner = InteractiveGameRunner(number_of_players)
    game_runner.run()


if __name__ == '__main__':
    argh.dispatch_command(main)
