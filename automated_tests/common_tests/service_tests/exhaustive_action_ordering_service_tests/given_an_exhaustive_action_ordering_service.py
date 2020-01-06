from abc import ABC
from unittest import TestCase


# noinspection PyPep8Naming
class Given_A_ExhaustiveActionOrderingService(TestCase, ABC):
    def setUp(self) -> None:
        self.SUT: ExhaustiveActionOrderingService = ExhaustiveActionOrderingService()
        self.because()

    def because(self) -> None:
        pass