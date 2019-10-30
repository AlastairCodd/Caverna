from abc import ABC
from unittest import TestCase

# noinspection PyPep8Naming
from buisness_logic.services.action_invoke_service import ActionInvokeService


class Given_A_ActionInvokeService(TestCase, ABC):
    def setUp(self) -> None:
        self.SUT: ActionInvokeService = ActionInvokeService()
        self.because()

    def because(self) -> None:
        pass
