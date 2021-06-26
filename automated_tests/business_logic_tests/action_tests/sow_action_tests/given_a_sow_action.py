from abc import ABCMeta
from unittest import TestCase

from buisness_logic.actions.sow_action import SowAction


# noinspection PyPep8Naming
class Given_A_SowAction(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: SowAction = SowAction()
        self.because()

    def because(self) -> None:
        pass
