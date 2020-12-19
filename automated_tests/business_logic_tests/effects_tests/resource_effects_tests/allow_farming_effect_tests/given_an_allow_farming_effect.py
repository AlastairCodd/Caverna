from abc import ABCMeta
from unittest import TestCase

from buisness_logic.effects.resource_effects import AllowFarmingEffect


# noinspection PyPep8Naming


class Given_An_AllowFarmingEffect(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: AllowFarmingEffect = AllowFarmingEffect()
        self.because()

    def because(self) -> None:
        pass
