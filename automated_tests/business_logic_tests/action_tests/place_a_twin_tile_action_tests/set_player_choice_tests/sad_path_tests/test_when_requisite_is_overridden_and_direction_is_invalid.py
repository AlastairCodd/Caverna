from typing import Dict, List, Optional

from automated_tests.business_logic_tests.action_tests.place_a_twin_tile_action_tests.given_a_place_a_twin_tile_action \
    import Given_A_PlaceATwinTileAction
from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests \
    .given_a_complete_dwarf_player_choice_transfer_service import FakeCard
from automated_tests.mocks.mock_card import MockCard
from automated_tests.mocks.mock_player import MockPlayer
from buisness_logic.tiles.dwelling import Dwelling
from buisness_logic.tiles.game_change_tiles import OfficeRoomTile
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.result_lookup import ResultLookup
from common.entities.tile_twin_placement_lookup import TileTwinPlacementLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_tile import BaseTile
from core.enums.caverna_enums import ResourceTypeEnum, TileDirectionEnum, TileTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService


class test_when_requisite_is_overridden_and_direction_is_invalid(Given_A_PlaceATwinTileAction):
    def because(self) -> None:
        self.initialise_sut_with_twin_tile(TileTypeEnum.cavernTunnelTwin)

        self._player: BasePlayerService = self.initialise_player()

        turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup(
            [FakeCard()],
            [Dwelling()],
            1,
            2,
            HarvestTypeEnum.Harvest)

        self._result: ResultLookup[ActionChoiceLookup] = self.SUT.set_player_choice(
            self._player,
            self._dwarf_to_use,
            turn_descriptor
        )

        self._action_invoked_result: ResultLookup[int] = self.SUT.invoke(
            self._player,
            None,  # Unused for this action
            self._dwarf_to_use  # Unused for this action
        )

    def initialise_player(self) -> BasePlayerService:
        self._dwarf_to_use: Dwarf = Dwarf(True)

        active_dwarf_1: Dwarf = Dwarf(True)
        active_dwarf_1.set_active(MockCard())

        active_dwarf_2: Dwarf = Dwarf(True)
        active_dwarf_2.set_active(MockCard())

        dwarves: List[Dwarf] = [active_dwarf_1, self._dwarf_to_use, active_dwarf_2]

        self._starting_resources: Dict[ResourceTypeEnum, int] = {
            ResourceTypeEnum.wood: 4,
            ResourceTypeEnum.stone: 3,
            ResourceTypeEnum.ruby: 1,
        }

        player: MockPlayer = MockPlayer(dwarves, self._starting_resources)

        office_room: BaseTile = OfficeRoomTile()
        player.tiles[1].set_tile(office_room)

        # _ 1 2 _ | _ _ _ 7
        # 8 x x x | x x x _
        # _ x x x | x x x _
        # _ x x x | C x x _
        # _ x x x | D x x _
        # _ _ _ _ | _4546 _
        location_to_place_primary_tile: int = 45
        location_to_place_secondary_tile: int = location_to_place_primary_tile + 1

        player.get_player_choice_location_to_build_twin_returns(
            lambda _, __: ResultLookup(
                True,
                TileTwinPlacementLookup(location_to_place_primary_tile, TileDirectionEnum.right)))

        player.get_player_choice_effects_to_use_for_cost_discount_returns(lambda _, __: {})

        self._expected_tiles: Dict[int, BaseTile] = {
            1: office_room,
            location_to_place_primary_tile: None,
            location_to_place_secondary_tile: None,
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

    def test_then_invoked_result_flag_should_be_false(self) -> None:
        self.assertFalse(self._action_invoked_result.flag)

    def test_then_invoked_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._action_invoked_result.value)

    def test_then_invoked_result_value_should_be_expected(self) -> None:
        self.assertEqual(self._action_invoked_result.value, 0)

    def test_then_invoked_result_errors_should_not_be_empty(self) -> None:
        self.shouldNotBeEmpty(self._action_invoked_result.errors)

    def test_then_player_should_have_tiles_at_expected_locations(self) -> None:
        for tile_location in self._expected_tiles:
            with self.subTest(location=tile_location):
                expected_tile: Optional[BaseTile] = self._expected_tiles[tile_location]
                if expected_tile is not None:
                    self.assertIs(self._player.tiles[tile_location].tile.id, expected_tile.id)
                else:
                    self.assertIsNone(self._player.tiles[tile_location].tile)

    def test_then_player_should_have_expected_amount_of_resources(self) -> None:
        for resource in self._starting_resources:
            with self.subTest(resource=resource):
                expected_amount: int = self._starting_resources[resource]
                if expected_amount == 0:
                    self.assertNotIn(resource, self._player.resources)
                else:
                    self.assertEqual(self._player.resources[resource], expected_amount)
