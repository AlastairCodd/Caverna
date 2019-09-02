from abc import ABC
from unittest import TestCase

from buisness_logic.validators.partition_resource_validator import PartitionResourceValidator


# noinspection PyPep8Naming
class Given_A_PartitionResourceValidator(TestCase, ABC):
    def setUp(self) -> None:
        self.SUT: PartitionResourceValidator = PartitionResourceValidator()
        self.because()

    def because(self) -> None:
        pass
