from typing import List

from automated_tests.common_tests.service_tests.conditional_service_tests.test_conditionalService import Given_A_Conditional_Service
from buisness_logic.cards.ore_trading_card import OreTradingCard
from common.entities.action_choice_lookup import ActionChoiceLookup


class test_when_card_is_ore_trading_card(Given_A_Conditional_Service):
    def because(self) -> None:
        card: OreTradingCard = OreTradingCard()

        self._result: List[ActionChoiceLookup] = self.SUT.get_possible_choices(card.actions)

    def test_then_result_should_not_be_null(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_should_not_be_empty(self) -> None:
        self.assertGreater(len(self._result), 0)

    def test_then_result_should_contain_expected_number_of_possible_action_choices(self) -> None:
        self.assertEqual(len(self._result), 3)