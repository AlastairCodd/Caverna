from abc import ABC
from unittest import TestCase


# noinspection PyPep8Naming
from common.services.exhaustive_action_ordering_service import ExhaustiveActionOrderingService


class Given_An_ExhaustiveActionOrderingService(TestCase, ABC):
    def setUp(self) -> None:
        self.SUT: ExhaustiveActionOrderingService = ExhaustiveActionOrderingService()
        self.because()

    def because(self) -> None:
        pass
