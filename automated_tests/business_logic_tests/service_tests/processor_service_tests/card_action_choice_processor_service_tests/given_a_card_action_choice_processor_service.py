from abc import ABCMeta
from unittest import TestCase

from buisness_logic.services.processor_services.card_action_choice_processor_service import CardActionChoiceProcessorService


# noinspection PyPep8Naming
class Given_A_CardActionChoiceProcessorService(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: CardActionChoiceProcessorService = CardActionChoiceProcessorService()
        self.because()

    def because(self) -> None:
        pass
