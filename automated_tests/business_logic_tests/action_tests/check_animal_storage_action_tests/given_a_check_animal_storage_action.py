from abc import ABCMeta
from unittest import TestCase

from buisness_logic.actions.check_animal_storage_action import CheckAnimalStorageAction


class Given_A_CheckAnimalStorageAction(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: CheckAnimalStorageAction = CheckAnimalStorageAction()

        self.because()

    def because(self) -> None:
        pass
