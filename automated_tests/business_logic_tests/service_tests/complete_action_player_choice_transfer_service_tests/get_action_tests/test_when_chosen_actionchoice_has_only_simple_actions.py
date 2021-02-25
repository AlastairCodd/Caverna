from typing import List

from automated_tests.business_logic_tests.service_tests.complete_action_player_choice_transfer_service_tests. \
    given_a_complete_action_player_choice_transfer_service import Given_A_CompleteActionPlayerChoiceTransferService
from automated_tests.business_logic_tests.service_tests.complete_dwarf_player_choice_transfer_service_tests. \
    given_a_complete_dwarf_player_choice_transfer_service import NullAction, FakeCard
from automated_tests.mocks.mock_player import MockPlayer
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.dwarf import Dwarf
from common.entities.multiconditional import Conditional
from common.entities.precedes_constraint import PrecedesConstraint
from common.entities.result_lookup import ResultLookup
from common.entities.turn_descriptor_lookup import TurnDescriptorLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_constraint import BaseConstraint
from core.enums.caverna_enums import ActionCombinationEnum
from core.enums.harvest_type_enum import HarvestTypeEnum


class test_when_chosen_actionchoice_has_only_simple_actions(Given_A_CompleteActionPlayerChoiceTransferService):
    def because(self) -> None:
        mock_player = MockPlayer()
        mock_player.get_player_choice_actions_to_use_returns(self.action_choice_selection)

        dwarf: Dwarf = Dwarf()

        base_action_1: BaseAction = NullAction()
        base_action_2: BaseAction = NullAction()

        # [[base_action_1,base_action_2], [base_action_2]]
        card_action_conditional: Conditional = Conditional(
            ActionCombinationEnum.AndThenOr,
            base_action_1,
            base_action_2)

        card: BaseCard = FakeCard(actions=card_action_conditional)
        # parameter is unused by current actions
        cards: List[BaseCard] = [card]

        self._expected_actions: List[BaseAction] = [
            base_action_1,
            base_action_2
        ]

        self._expected_constraints: List[BaseConstraint] = [
            PrecedesConstraint(base_action_1, base_action_2)
        ]

        self._expected_result: ActionChoiceLookup = ActionChoiceLookup(
            self._expected_actions,
            self._expected_constraints)

        turn_descriptor: TurnDescriptorLookup = TurnDescriptorLookup(
            cards,
            [],
            0,
            2,
            HarvestTypeEnum.NoHarvest)

        self._result: ResultLookup[ActionChoiceLookup] = self.SUT.get_action(
            mock_player,
            dwarf,
            card,
            turn_descriptor)

    # noinspection PyUnusedLocal
    def action_choice_selection(
            self,
            possible_actions: List[ActionChoiceLookup],
            turn_descriptor: TurnDescriptorLookup) -> ResultLookup[ActionChoiceLookup]:
        return ResultLookup(True, possible_actions[0])

    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_true(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result.value)

    def test_then_result_value_should_match_expected(self) -> None:
        self.assertEqual(self._result.value, self._expected_result)

    def test_then_result_value_actions_should_not_be_empty(self) -> None:
        self.assertGreater(len(self._result.value.actions), 0)

    def test_then_result_value_actions_should_have_expected_number_of_actions(self) -> None:
        self.assertEqual(len(self._result.value.actions), len(self._expected_actions))

    def test_then_result_value_actions_should_contain_expected_simple_actions(self) -> None:
        action: BaseAction
        for action in self._expected_actions:
            with self.subTest(action=action):
                self.assertIn(action, self._result.value.actions)

    def test_then_result_value_constraints_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result.value.constraints)

    def test_then_result_value_constraints_should_not_be_empty(self) -> None:
        self.assertGreater(len(self._result.value.constraints), 0)

    def test_then_result_value_constraints_should_have_expected_number_of_constraints(self) -> None:
        self.assertEqual(len(self._result.value.constraints), len(self._expected_constraints))

    def test_then_result_value_constraints_should_contain_expected_simple_constraints(self) -> None:
        constraint: BaseConstraint
        for constraint in self._expected_constraints:
            with self.subTest(constraint=constraint):
                self.assertIn(constraint, self._result.value.constraints)
