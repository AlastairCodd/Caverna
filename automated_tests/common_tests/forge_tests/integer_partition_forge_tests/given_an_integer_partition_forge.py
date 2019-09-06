from abc import ABC
from unittest import TestCase

from common.forges.integer_partition_forge import IntegerPartitionForge


class Given_An_IntegerPartitionForge(TestCase, ABC):
    def setUp(self):
        self.SUT: IntegerPartitionForge = IntegerPartitionForge()
        self.because()

    def because(self):
        pass
