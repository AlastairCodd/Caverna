from abc import ABCMeta
from unittest import TestCase

from buisness_logic.services.processor_services.conversions_to_perform_action_choice_processor_service import ConversionsToPerformActionChoiceProcessorService


# noinspection PyPep8Naming
class Given_A_ConversionsToPerformActionChoiceProcessorService(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: ConversionsToPerformActionChoiceProcessorService = ConversionsToPerformActionChoiceProcessorService()
        self.because()

    def because(self) -> None:
        pass
