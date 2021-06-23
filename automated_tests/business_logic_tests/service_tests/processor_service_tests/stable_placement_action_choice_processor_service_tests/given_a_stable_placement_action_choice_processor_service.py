from abc import ABCMeta
from unittest import TestCase

from buisness_logic.services.processor_services.stable_placement_action_choice_processor_service import StablePlacementActionChoiceProcessorService


# noinspection PyPep8Naming

class Given_A_StablePlacementActionChoiceProcessorService(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: StablePlacementActionChoiceProcessorService = StablePlacementActionChoiceProcessorService()
        self.because()

    def because(self) -> None:
        pass
