from abc import ABCMeta
from unittest import TestCase


# noinspection PyPep8Naming
from buisness_logic.actions.convert_action import ConvertAction


class Given_A_ConvertAction(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: ConvertAction = ConvertAction()
        self.because()

    def because(self) -> None:
        pass
