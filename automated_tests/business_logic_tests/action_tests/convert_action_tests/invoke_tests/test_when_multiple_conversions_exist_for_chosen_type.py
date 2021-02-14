from typing import cast, List

from automated_tests.business_logic_tests.action_tests.convert_action_tests.given_a_convert_action import Given_A_ConvertAction
from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests\
    .given_a_complete_dwarf_player_choice_transfer_service import FakeCard
from automated_tests.mocks.mock_player import MockPlayer
from buisness_logic.actions.convert_single_action import ConvertSingleAction
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.enums.caverna_enums import ResourceTypeEnum
from core.enums.harvest_type_enum import HarvestTypeEnum
from core.services.base_player_service import BasePlayerService


class test_when_multiple_conversions_exist_for_chosen_type(Given_A_ConvertAction):
    # noinspection PyTypeChecker
    def because(self) -> None:
        player: BasePlayerService = self.initialise_player()

        turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup(
            [FakeCard()],
            [],
            0,
            1,
            HarvestTypeEnum.Harvest)

        self._result: ResultLookup[ActionChoiceLookup] = self.SUT.set_player_choice(
            player,
            None,
            turn_descriptor)

        self._action_invoke_result: ResultLookup[int] = self.SUT.invoke(
            player,
            None,
            None)

        self._expected_conversions: List[BaseAction] = [
            ConvertSingleAction([ResourceTypeEnum.donkey], [ResourceTypeEnum.food], 3)
        ]

    def initialise_player(self) -> BasePlayerService:
        player: MockPlayer = MockPlayer()

        player.get_player_choice_conversions_to_perform_returns(lambda _: [([ResourceTypeEnum.donkey], 3, [ResourceTypeEnum.food])])

        return player

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result.value)

    def test_then_result_value_actions_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result.value.actions)

    def test_then_result_value_actions_should_not_be_empty(self) -> None:
        self.assertGreater(len(cast(List, self._result.value.actions)), 0)

    def test_then_result_value_actions_should_contain_expected_conversions(self) -> None:
        for conversion in self._expected_conversions:
            with self.subTest(conversions=conversion):
                self.assertIn(conversion, self._result.value.actions)

    def test_then_result_errors_should_be_empty(self) -> None:
        self.assertListEqual(cast(list, self._result.errors), [])

    def test_then_action_invoke_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._action_invoke_result)

    def test_then_action_invoke_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._action_invoke_result.flag)

    def test_then_action_invoke_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._action_invoke_result.value)

    def test_then_action_invoke_result_value_should_be_expected(self) -> None:
        self.assertEqual(self._action_invoke_result.value, 0)

    def test_then_action_invoke_result_errors_should_be_empty(self) -> None:
        self.assertListEqual(cast(list, self._action_invoke_result.errors), [])
