from abc import ABCMeta
from unittest import TestCase

from buisness_logic.actions.breed_animals_action import BreedAnimalsAction


class Given_A_BreedAnimalsAction(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: BreedAnimalsAction = BreedAnimalsAction(3)

        self.because()

    def because(self) -> None:
        pass
