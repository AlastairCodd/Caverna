from abc import ABCMeta
from unittest import TestCase

from common.entities.multi_variable_polynomial import MultiVariablePolynomial


# noinspection PyPep8Naming
class Given_A_MultiVariablePolynomial(TestCase, metaclass=ABCMeta):
    def setUp(self) -> None:
        self.SUT: MultiVariablePolynomial
        self.because()

    def because(self) -> None:
        pass
