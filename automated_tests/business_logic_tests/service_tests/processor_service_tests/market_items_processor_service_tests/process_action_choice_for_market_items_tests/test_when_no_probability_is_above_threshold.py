from automated_tests.business_logic_tests.service_tests.processor_service_tests.market_items_processor_service_tests.given_a_market_items_to_purchase_action_choice_processor_service import \
    Given_A_MarketItemsToPurchaseActionChoiceProcessorService
from buisness_logic.services.processor_services.market_items_to_purchase_action_choice_processor_service import MarketItemActionChoice


class test_when_no_probability_is_above_threshold(Given_A_MarketItemsToPurchaseActionChoiceProcessorService):
    def because(self) -> None:
        self.SUT.offset = 0
        self.SUT.set_action_choice([0.1 for _ in range(self.SUT.length)])

        self._result: MarketItemActionChoice = self.SUT.process_action_choice_for_market_items()
        
    def test_then_result_should_not_be_none(self) -> None:
        self.assertIsNotNone(self._result)

    def test_then_result_hashcode_should_be_zero(self) -> None:
        self.assertEqual(self._result.hashcode, 0)

    def test_then_result_items_to_purchase_should_be_empty(self) -> None:
        self.assertEqual(len(self._result.items_to_purchase), 0)
