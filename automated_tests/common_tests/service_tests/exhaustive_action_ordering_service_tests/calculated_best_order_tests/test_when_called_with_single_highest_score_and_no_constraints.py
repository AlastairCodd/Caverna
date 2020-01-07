from typing import List, Dict

from automated_tests.common_tests.service_tests.exhaustive_action_ordering_service_tests.given_an_exhaustive_action_ordering_service import \
    Given_An_ExhaustiveActionOrderingService
from automated_tests.mocks.mock_player import MockPlayer
from common.entities.action_choice_lookup import ActionChoiceLookup
from common.entities.player import Player
from common.entities.result_lookup import ResultLookup
from core.baseClasses.base_action import BaseAction
from core.baseClasses.base_card import BaseCard
from core.baseClasses.base_constraint import BaseConstraint
from core.enums.caverna_enums import ResourceTypeEnum


class Test_When_Called_With_Single_Highest_Score_And_No_Constraints(Given_An_ExhaustiveActionOrderingService):
    def because(self) -> None:
        action1: BaseAction = None
        action2: BaseAction = None
        action3: BaseAction = None

        actions: List[BaseAction] = []
        constraints: List[BaseConstraint] = []
        action_choice_lookup: ActionChoiceLookup = ActionChoiceLookup(actions, constraints)

        self._expected_best_ordering: List[BaseAction] = [action1, action2, action3]

        resources: Dict[ResourceTypeEnum, int] = {}

        player: Player = MockPlayer(3,resources=resources)
        current_card: BaseCard = None
        current_dwarf: Dwarf = None

        self._result: ResultLookup[List[BaseAction]] = self.SUT.calculated_best_order(
            action_choice_lookup,
            player,
            current_card,
            current_dwarf)

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_flag_should_be_expected(self) -> None:
        self.assertTrue(self._result.flag)

    def test_then_result_value_should_be_in_expected_order(self) -> None:
        self.assertListEqual(self._result.value, self._expected_best_ordering)