from typing import Dict, List, cast, Optional

from automated_tests.business_logic_tests.action_tests.place_a_single_tile_action_tests \
    .given_a_place_a_single_tile_action import Given_A_PlaceASingleTileAction
from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests \
    .given_a_complete_dwarf_player_choice_transfer_service import FakeCard
from automated_tests.mocks.mock_card import MockCard
from automated_tests.mocks.mock_player import MockPlayer
from buisness_logic.tiles.dwelling import Dwelling
from buisness_logic.tiles.point_tiles import BroomChamberTile, TreasureChamberTile
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.tile_unknown_placement_lookup import TileUnknownPlacementLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum, TileTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService


class test_when_requisites_are_overridden(Given_A_PlaceASingleTileAction):
    def because(self) -> None:
        self.initialise_sut_as_tile_type_which_is_not_specific([TileTypeEnum.forest])

        tiles: List[BaseTile] = [Dwelling(), BroomChamberTile(), TreasureChamberTile()]
        self._player: BasePlayerService = self.initialise_player(tiles)

        self._turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup(
            [FakeCard()],
            tiles,
            1,
            2,
            HarvestTypeEnum.Harvest)

        self._result: ResultLookup[ActionChoiceLookup] = self.SUT.set_player_choice(
            self._player,
            self._dwarf_to_use,
            self._turn_descriptor
        )

        self._expected_resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.wood: 0,
            ResourceTypeEnum.stone: 0,
            ResourceTypeEnum.ruby: 1,
        }

        self._action_invoked_result: ResultLookup[int] = self.SUT.invoke(
            self._player,
            None,  # Unused for this action
            self._dwarf_to_use  # Unused for this action
        )

    def initialise_player(
            self,
            tiles: List[BaseTile]) -> BasePlayerService:
        self._dwarf_to_use: Dwarf = Dwarf(True)

        active_dwarf_1: Dwarf = Dwarf(True)
        active_dwarf_1.set_active(MockCard())

        active_dwarf_2: Dwarf = Dwarf(True)
        active_dwarf_2.set_active(MockCard())

        dwarves: List[Dwarf] = [active_dwarf_1, self._dwarf_to_use, active_dwarf_2]

        starting_resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.wood: 4,
            ResourceTypeEnum.stone: 3,
            ResourceTypeEnum.ruby: 1,
        }

        player: MockPlayer = MockPlayer(dwarves, starting_resources)
        # _ 1 2 _ | _ _ _ 7
        # 8 x x x | x x x _
        # _ x x x | x _ x _
        # _ x x x | C _ x _
        # _ x x35 | D x x _
        # _ _ _ _ | _ _ _ _
        location_to_place_tile: int = 35
        player.get_player_choice_location_to_build_returns(
            lambda _, __, ___: ResultLookup(
                True,
                TileUnknownPlacementLookup(location_to_place_tile, None)))

        self._tile_to_build: BaseTile = tiles[0]
        player.get_player_choice_tile_to_build_returns(
            lambda _, __: ResultLookup(True, self._tile_to_build)
        )

        player.get_player_choice_effects_to_use_for_cost_discount_returns(lambda _, __: {})

        self._expected_tiles: Dict[int, BaseTile] = {
            location_to_place_tile: self._tile_to_build
        }

        return player

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result.value)

    def test_then_result_value_should_have_no_actions(self) -> None:
        self.assertEqual(len(self._result.value.actions), 0)

    def test_then_result_value_should_have_no_constraints(self) -> None:
        self.assertEqual(len(self._result.value.constraints), 0)

    def test_then_invoked_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._action_invoked_result)

    def test_then_invoked_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._action_invoked_result.flag)

    def test_then_invoked_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._action_invoked_result.value)

    def test_then_invoked_result_value_should_be_expected(self) -> None:
        self.assertEqual(self._action_invoked_result.value, 1)

    def test_then_invoked_result_errors_should_be_empty(self) -> None:
        self.assertListEqual([], cast(List, self._action_invoked_result.errors))

    def test_then_player_should_have_tiles_at_expected_locations(self) -> None:
        for tile_location in self._expected_tiles:
            with self.subTest(location=tile_location):
                expected_tile: Optional[BaseTile] = self._expected_tiles[tile_location]
                if expected_tile is not None:
                    self.assertIs(self._player.tiles[tile_location].tile, expected_tile)
                else:
                    self.assertIsNone(self._player.tiles[tile_location].tile)

    def test_then_player_should_have_expected_amount_of_resources(self) -> None:
        for resource in self._expected_resources:
            with self.subTest(resource=resource):
                expected_amount: int = self._expected_resources[resource]
                if expected_amount == 0:
                    self.assertNotIn(resource, self._player.resources)
                else:
                    self.assertEqual(self._player.resources[resource], expected_amount)

    def test_then_tile_service_should_report_tile_is_not_available(self) -> None:
        self.assertFalse(self.SUT._tile_service.is_tile_available(
            self._turn_descriptor,
            self._tile_to_build))
