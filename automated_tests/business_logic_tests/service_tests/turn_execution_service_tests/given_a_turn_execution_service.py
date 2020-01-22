from abc import ABC
from unittest import TestCase


# noinspection PyPep8Naming
from buisness_logic.services.turn_execution_service import TurnExecutionService


class Given_A_TurnExecutionService(TestCase, ABC):
    def setUp(self) -> None:
        self.SUT: TurnExecutionService = TurnExecutionService()
        self.because()

    def because(self) -> None:
        pass
