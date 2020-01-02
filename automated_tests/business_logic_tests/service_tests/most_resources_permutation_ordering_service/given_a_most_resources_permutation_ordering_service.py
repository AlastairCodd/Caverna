from abc import ABC
from unittest import TestCase

# noinspection PyPep8Naming
from buisness_logic.services.most_resources_permutation_ordering_service import MostResourcesPermutationOrderingService
from core.baseClasses.base_permutation_ordering_service import BasePermutationOrderingService


class Given_A_MostResourcesPermutationOrderingService(TestCase, ABC):
    def setUp(self) -> None:
        self.SUT: BasePermutationOrderingService = MostResourcesPermutationOrderingService()
        self.because()

    def because(self) -> None:
        pass
