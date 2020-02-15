from abc import ABC
from unittest import TestCase


# noinspection PyPep8Naming
from common.forges.list_permutation_forge import ListPermutationForge


class Given_A_ListPermutationForge(TestCase, ABC):
    def setUp(self) -> None:
        self.SUT: ListPermutationForge = ListPermutationForge()
        self.because()

    def because(self) -> None:
        pass
