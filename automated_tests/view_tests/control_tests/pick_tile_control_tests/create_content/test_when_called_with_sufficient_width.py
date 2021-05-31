from typing import List, Dict

from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.layout import UIContent

from automated_tests.view_tests.control_tests.pick_tile_control_tests.given_a_pick_tile_control import Given_A_PickTileControl
from buisness_logic.effects.allow_farming_effect import AllowFarmingEffect
from buisness_logic.tiles.animal_storage_tiles import BreakfastRoomTile
from buisness_logic.tiles.dwelling import Dwelling, MixedDwelling
from buisness_logic.tiles.game_change_tiles import GuestRoomTile
from buisness_logic.tiles.mine_tiles import CavernTile, TunnelTile, DeepTunnelTile, OreMineTile
from buisness_logic.tiles.outdoor_tiles import FieldTile, MeadowTile, PastureTile
from buisness_logic.tiles.point_tiles import BroomChamberTile, WeavingParlorTile
from common.repositories.simple_player_repository import SimplePlayerRepository
from core.baseClasses.base_tile import BaseTile
from core.containers.tile_container import TileContainer
from core.enums.caverna_enums import ResourceTypeEnum


class test_when_called_with_sufficient_width(Given_A_PickTileControl):
    def because(self) -> None:
        tile_container: TileContainer = self._get_tile_container()

        self.SUT.set_tile_container(tile_container)

        self._content: UIContent = self.SUT.create_content(0, 0)

        self._expected_lines: List[str] = [
            "┌───│00│─────┬───│01│─────┬───│02│─────┬───│03│─────┬───│04│─────┬───│05│─────┬───│06│─────┬───│07│─────┐",
            "│ N/A        │ N/A        │ N/A        │ N/A        │ N/A        │ N/A        │ N/A        │ N/A        │",
            "│            │            │            │            │            │            │            │            │",
            "│            │            │            │            │            │            │            │            │",
            "├───│08│─────┼───│09│─────┼───│10│─────┼───│11│─────┼───│12│─────┼───│13│─────┼───│14│─────┼───│15│─────┤",
            "│ N/A        │ Forest     │ Meadow     │ Field      │ Breakfast  │ Broom      │ Dwelling   │ N/A        │",
            "│            │            │            │ 3 grain    │ Room       │ Chamber    │            │            │",
            "│            │            │            │            │            │            │            │            │",
            "├───│16│─────┼───│17│─────┼───│18│─────┼───│19│─────┼───│20│─────┼───│21│─────┼───│22│─────┼───│23│─────┤",
            "│ N/A        │ Forest     │ Meadow     │ Field      │ Cavern     │ Tunnel     │ Weaving    │ N/A        │",
            "│            │            │            │ 2 veg      │            │            │ Parlor     │            │",
            "│            │            │            │            │            │            │            │            │",
            "├───│24│─────┼───│25│─────┼───│26│─────┼───│27│─────┼───│28│─────┼───│29│─────┼───│30│─────┼───│31│─────┤",
            "│ N/A        │ Meadow     │ Meadow     │ Pasture    │ Dwelling   │ Deep       │ Mixed      │ N/A        │",
            "│            │            │            │            │            │ Tunnel     │ Dwelling   │            │",
            "│            │            │            │            │            │            │            │            │",
            "├───│32│─────┼───│33│─────┼───│34│─────┼───│35│─────┼───│36│─────┼───│37│─────┼───│38│─────┼───│39│─────┤",
            "│ N/A        │ Forest     │ Field      │ Field      │ Entry      │ Ore        │ Guest      │ N/A        │",
            "│            │            │            │            │ Level      │ Mine       │ Room       │            │",
            "│            │            │            │            │ Dwelling   │            │            │            │",
            "├───│40│─────┼───│41│─────┼───│42│─────┼───│43│─────┼───│44│─────┼───│45│─────┼───│46│─────┼───│47│─────┤",
            "│ N/A        │ N/A        │ N/A        │ N/A        │ N/A        │ N/A        │ N/A        │ N/A        │",
            "│            │            │            │            │            │            │            │            │",
            "│            │            │            │            │            │            │            │            │",
            "└────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────┘", ]

    def _get_tile_container(self) -> TileContainer:
        result: SimplePlayerRepository = SimplePlayerRepository(0, "Tile Container", 0)
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

        resources_at_location: Dict[int, ResourceTypeEnum] = {
            11: ResourceTypeEnum.grain,
            19: ResourceTypeEnum.veg,
        }

        for location, tile in tile_and_location.items():
            result.tiles[location].set_tile(tile)

            if location in resources_at_location:
                resource: ResourceTypeEnum = resources_at_location[location]
                allow_farming_effects: List[AllowFarmingEffect] = result.tiles[location].get_effects_of_type(AllowFarmingEffect)
                result.give_resource(resource, 1)
                allow_farming_effects[0].plant_resource(result, resource)

        return result

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._content)

    def test_then_result_number_of_lines_should_be_expected(self) -> None:
        self.assertEqual(len(self._expected_lines), self._content.line_count)

    def test_then_result_get_lines_should_contain_expected_lines(self) -> None:
        for line_index, line in enumerate(self._expected_lines):
            with self.subTest(lines=line):
                formatted_text: StyleAndTextTuples = self._content.get_line(line_index)
                plaintext: str = self._get_plaintext(formatted_text)
                self.assertIn(line, plaintext)

    def _get_plaintext(self, formatted_text: StyleAndTextTuples) -> str:
        return formatted_text[0][1]
