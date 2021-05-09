from random import randrange, choice
from typing import List, Dict, Tuple

from prompt_toolkit import Application, HTML
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import VSplit, HSplit, Window, BufferControl, FormattedTextControl, Layout
from prompt_toolkit.layout.containers import Container
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Frame

from buisness_logic.tiles.animal_storage_tiles import BreakfastRoomTile
from buisness_logic.tiles.dwelling import Dwelling, MixedDwelling
from buisness_logic.tiles.game_change_tiles import GuestRoomTile
from buisness_logic.tiles.mine_tiles import CavernTile, TunnelTile, DeepTunnelTile, OreMineTile
from buisness_logic.tiles.outdoor_tiles import FieldTile, MeadowTile, PastureTile
from buisness_logic.tiles.point_tiles import BroomChamberTile, WeavingParlorTile
from common.formatters.resource_container_formatter import ResourceContainerFormatter
from common.formatters.tile_container_formatter import TileContainerFormatter
from common.repositories.simple_player_repository import SimplePlayerRepository
from core.baseClasses.base_tile import BaseTile
from core.constants import html_tags
from core.enums.caverna_enums import ResourceTypeEnum
from core.repositories.base_player_repository import BasePlayerRepository


class ShellView(object):
    def __init__(self):
        bindings = KeyBindings()

        bindings.add("c-q")(self.close_app)
        bindings.add("c-c")(self.close_app)

        buffer1: Buffer = Buffer()  # Editable buffer.
        buffer2: Buffer = Buffer()  # Editable buffer.

        buffer1.insert_text("Master")
        buffer2.insert_text("Detail")

        # noinspection PyTypeChecker
        top_host: Container = VSplit([
            # One window that holds the BufferControl with the default buffer on
            # the left.
            Frame(
                Window(content=BufferControl(buffer=buffer1)),
                title="Master"),

            # A vertical line in the middle. We explicitly specify the width, to
            # make sure that the layout engine will not try to divide the whole
            # width by three for all these windows. The window will simply fill its
            # content by repeating this character.
            # Window(width=1, char='|'),

            # Display the text 'Hello world' on the right.
            Frame(
                Window(content=BufferControl(buffer=buffer2)),
                title="Detail"),
        ])

        player, resources_delta = self._temp_initialise_random_player()

        resource_container_formatter: ResourceContainerFormatter = ResourceContainerFormatter()
        resource_text: str = resource_container_formatter.format(player, resources_delta)
        # stone: 3  (+3)       coin: 2  (-1)

        # noinspection PyTypeChecker
        resource_container: Container = Frame(
            Window(FormattedTextControl(HTML(resource_text))),
            title="Resources")

        tile_container_formatter: TileContainerFormatter = TileContainerFormatter()
        board_text: str = tile_container_formatter.format(player, [x for x in range(8, 39) if x % 8 != 0 and x % 8 != 7])

        # noinspection PyTypeChecker
        board_container: Container = Frame(
            Window(FormattedTextControl(HTML(board_text))),
            title="Board")

        player_host: Container = VSplit([resource_container, board_container])

        main_host: Container = HSplit([
            top_host,
            Frame(
                player_host,
                title="Player Representation")
        ])

        layout: Layout = Layout(main_host)

        self._app: Application = Application(
            key_bindings=bindings,
            full_screen=True,
            layout=layout,
            style=Style.from_dict(
                {
                    html_tags.resource_delta: "#e09d00",
                    html_tags.tile_type_unavailable: "#8a8c89",
                    html_tags.tile_type_forest: "#27680b",
                    html_tags.tile_type_underground: "#a9664b",
                    html_tags.tile_type_meadow: "#76d37e",
                    html_tags.tile_type_field: "#d3b976",
                    html_tags.tile_type_cavern: "#afafae",
                    html_tags.tile_type_tunnel: "#afafae",
                    html_tags.tile_type_deepTunnel: "#544c4a",
                    html_tags.tile_type_pasture: "#d3b976",
                    html_tags.tile_type_furnishedCavern: "#ea7344",
                    html_tags.tile_type_furnishedDwelling: "#4491ea",
                    html_tags.tile_type_oreMine: "#6b737c",
                    html_tags.tile_type_rubyMine: "#7c6b6c",
                }
            )
        )
        self._app.run()

    def close_app(self, _) -> None:
        self._app.exit(result=True)

    def _temp_initialise_random_player(self):
        player: BasePlayerRepository = SimplePlayerRepository(0, "player", 0)
        player_resources: Dict[ResourceTypeEnum, int] = {}
        resources_delta: Dict[ResourceTypeEnum, int] = {}
        for resource in ResourceTypeEnum:
            if resource != ResourceTypeEnum.begging_marker:
                amount: int = randrange(0, 12)
                extra_amount: int = 0 if choice([True, False]) else randrange(-3, 3)

                player_resources[resource] = amount
                if extra_amount != 0:
                    resources_delta[resource] = extra_amount
        player.give_resources(player_resources)

        tile_and_location: Dict[int, BaseTile] = {
            # 9: None,
            10: MeadowTile(),
            11: FieldTile(),
            12: BreakfastRoomTile(),
            13: BroomChamberTile(),
            14: Dwelling(),

            # 17: None,
            18: MeadowTile(),
            19: FieldTile(),
            20: CavernTile(),
            21: TunnelTile(),
            22: WeavingParlorTile(),

            25: MeadowTile(),
            26: MeadowTile(),
            27: PastureTile(),
            28: Dwelling(),
            29: DeepTunnelTile(),
            30: MixedDwelling(),

            # 33: None,
            34: FieldTile(),
            35: FieldTile(),
            # 36: EntryLevelDwelling(),
            37: OreMineTile(),
            38: GuestRoomTile(),
        }

        for location, tile in tile_and_location.items():
            player.tiles[location].set_tile(tile)

        return player, resources_delta
