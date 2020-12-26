from abc import ABC, abstractmethod
from unittest import TestCase

from buisness_logic.actions.get_a_baby_dwarf_action import GetABabyDwarfAction


# noinspection PyPep8Naming
class Given_A_GetABabyDwarfAction(ABC, TestCase):
    def setUp(self) -> None:
        self.SUT: GetABabyDwarfAction = GetABabyDwarfAction()
        self.because()

    @abstractmethod
    def because(self):
        pass
