import argh

from view.shell_view import ShellView


@argh.arg('number_of_players', choices=list(range(2,8)))
def main(number_of_players: int) -> None:
    ShellView()


if __name__ == '__main__':
    argh.dispatch_command(main)
