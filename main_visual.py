import argh

from view.shell_view import ShellView


# @argh.arg('number_of_players', choices=list(range(2,8)))
# @argh.arg('show_tile_index', default=True)
@argh.arg('--use_compatible_characters', '-c', default=False)
def main(
        # number_of_players: int,
        use_compatible_characters: bool = False,
        show_tile_index: bool = True) -> None:
    ShellView(use_compatible_characters, show_tile_index)


if __name__ == '__main__':
    argh.dispatch_command(main)
