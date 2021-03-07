from abc import ABCMeta
from unittest import TestCase


# noinspection PyPep8Naming
from common.environments.caverna_env import CavernaEnv


class Given_A_CavernaEnv(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: CavernaEnv = CavernaEnv()
        self.because()

    def because(self) -> None:
        pass
