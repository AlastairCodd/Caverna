from abc import ABCMeta
from unittest import TestCase


# noinspection PyPep8Naming
from buisness_logic.effects.food_effects import SubstituteFoodForDwarfEffect
from core.enums.caverna_enums import ResourceTypeEnum


class Given_A_SubstituteFoodForDwarfEffect(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: SubstituteFoodForDwarfEffect = SubstituteFoodForDwarfEffect({ResourceTypeEnum.donkey: 2})
        self.because()

    def because(self) -> None:
        pass
