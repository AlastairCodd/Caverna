from typing import cast

from automated_tests.business_logic_tests.action_tests.sow_action_tests.given_a_sow_action import Given_A_SowAction
from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests.given_a_complete_dwarf_player_choice_transfer_service import \
    FakeCard
from automated_tests.mocks.mock_player import MockPlayer
from buisness_logic.tiles.dwelling import Dwelling
from buisness_logic.tiles.outdoor_tiles import FieldTile
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService


class test_when_sufficient_space_exists_for_all_resources(Given_A_SowAction):
    def because(self) -> None:
        player: BasePlayerService = self._initialise_player()

        turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup(
            [FakeCard()],
            [Dwelling()],
            1,
            2,
            HarvestTypeEnum.Harvest)

        self._result: ResultLookup[ActionChoiceLookup] = self.SUT.set_player_choice(
            player,
            None,
            turn_descriptor)

        self._action_invoke_result: ResultLookup[int] = self.SUT.invoke(
            player,
            None,
            None)

    def _initialise_player(self) -> BasePlayerService:
        player: MockPlayer = MockPlayer()
        player.get_player_choice_resources_to_sow_returns(lambda x, _: ResultLookup(True, [ResourceTypeEnum.veg for _ in range(x)]))

        player.tiles[0].set_tile(FieldTile())
        player.tiles[1].set_tile(FieldTile())
        player.tiles[2].set_tile(FieldTile())

        player.give_resource(ResourceTypeEnum.veg, 3)

        return player

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result.value)

    def test_then_result_value_actions_should_be_empty(self) -> None:
        self.assertEqual(len(self._result.value.actions), 0)

    def test_then_result_value_constraints_should_be_empty(self) -> None:
        self.assertEqual(len(self._result.value.constraints), 0)

    def test_then_result_errors_should_be_empty(self) -> None:
        self.assertListEqual(cast(list, self._result.errors), [])

    def test_then_action_invoke_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._action_invoke_result)

    def test_then_action_invoke_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._action_invoke_result.flag)

    def test_then_action_invoke_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._action_invoke_result.value)

    def test_then_action_invoke_result_value_should_be_expected(self) -> None:
        self.assertEqual(self._action_invoke_result.value, 3)

    def test_then_action_invoke_result_errors_should_be_empty(self) -> None:
        self.assertListEqual(cast(list, self._action_invoke_result.errors), [])
