from abc import ABCMeta
from unittest import TestCase

from buisness_logic.services.processor_services.animals_to_breed_action_choice_processor_service import AnimalsToBreedActionChoiceProcessorService


# noinspection PyPep8Naming
class Given_A_AnimalsToBreedActionChoiceProcessorService(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: AnimalsToBreedActionChoiceProcessorService = AnimalsToBreedActionChoiceProcessorService()
        self.because()

    def because(self) -> None:
        pass
