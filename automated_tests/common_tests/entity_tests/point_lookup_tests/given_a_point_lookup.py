from abc import ABCMeta
from unittest import TestCase

from common.entities.point_lookup import PointLookup


# noinspection PyPep8Naming
class Given_A_PointLookup(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: PointLookup
        self.because()

    def because(self) -> None:
        pass
