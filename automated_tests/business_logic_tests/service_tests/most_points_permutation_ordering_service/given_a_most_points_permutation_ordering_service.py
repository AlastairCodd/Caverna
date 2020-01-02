from abc import ABC
from unittest import TestCase

# noinspection PyPep8Naming
from buisness_logic.services.most_points_permutation_ordering_service import MostPointsPermutationOrderingService
from core.baseClasses.base_permutation_ordering_service import BasePermutationOrderingService


class Given_A_MostPointsPermutationOrderingService(TestCase, ABC):
    def setUp(self) -> None:
        self.SUT: BasePermutationOrderingService = MostPointsPermutationOrderingService()
        self.because()

    def because(self) -> None:
        pass
