from abc import ABCMeta
from unittest import TestCase


# noinspection PyPep8Naming
from buisness_logic.actions.convert_single_action import ConvertSingleAction
from core.enums.caverna_enums import ResourceTypeEnum


class Given_A_ConvertSingleAction(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: ConvertSingleAction = ConvertSingleAction(
            [ResourceTypeEnum.donkey],
            [ResourceTypeEnum.food],
            2)
        self.because()

    def because(self) -> None:
        pass
