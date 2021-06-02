from abc import ABCMeta
from unittest import TestCase

from buisness_logic.services.processor_services.twin_tile_placement_action_choice_processor_service import TwinTilePlacementActionChoiceProcessorService


# noinspection PyPep8Naming
class Given_A_TwinTilePlacementActionChoiceProcessorService(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: TwinTilePlacementActionChoiceProcessorService = TwinTilePlacementActionChoiceProcessorService()
        self.because()

    def because(self) -> None:
        pass
