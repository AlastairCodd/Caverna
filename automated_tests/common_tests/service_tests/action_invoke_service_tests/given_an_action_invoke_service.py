from abc import ABCMeta
from unittest import TestCase

from common.services.action_invoke_service import ActionInvokeService

# noinspection PyPep8Naming


class Given_An_ActionInvokeService(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: ActionInvokeService = ActionInvokeService()
        self.because()

    def because(self) -> None:
        pass
