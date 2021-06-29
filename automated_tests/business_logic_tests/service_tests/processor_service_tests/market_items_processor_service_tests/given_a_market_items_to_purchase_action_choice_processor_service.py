from abc import ABCMeta
from unittest import TestCase

from buisness_logic.services.processor_services.market_items_to_purchase_action_choice_processor_service import \
    MarketItemsToPurchaseActionChoiceProcessorService


# noinspection PyPep8Naming
class Given_A_MarketItemsToPurchaseActionChoiceProcessorService(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: MarketItemsToPurchaseActionChoiceProcessorService = MarketItemsToPurchaseActionChoiceProcessorService()
        self.because()

    def because(self) -> None:
        pass
