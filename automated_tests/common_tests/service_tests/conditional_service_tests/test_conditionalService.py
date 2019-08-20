from abc import abstractmethod, ABC
from unittest import TestCase
from common.services.conditional_service import ConditionalService


# noinspection PyPep8Naming
class Given_A_Conditional_Service(ABC, TestCase):
    def setUp(self) -> None:
        self.SUT: ConditionalService = ConditionalService()
        self.because()

    @abstractmethod
    def because(self):
        pass
