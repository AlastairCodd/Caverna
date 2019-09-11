from abc import ABC
from unittest import TestCase
from common.services.integer_partition_permutation_forge import IntegerPartitionPermutationForge


# noinspection PyPep8Naming
class Given_A_IntegerPartitionPermutationForge(TestCase, ABC):
    def setUp(self) -> None:
        self.SUT: IntegerPartitionPermutationForge = IntegerPartitionPermutationForge()
        self.because()

    def because(self) -> None:
        pass